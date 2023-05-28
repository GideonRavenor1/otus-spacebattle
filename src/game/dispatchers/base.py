import functools
import json
from collections.abc import Callable
from queue import Queue
from threading import Thread
from typing import Any

from pika.adapters.blocking_connection import BlockingChannel

from src.game.dependencies import container
from src.game.exceptions import AuthenticationException
from src.game.repositories.base import BaseRepository


def token_required(func: Callable) -> Callable:
    @functools.wraps(func)
    def _wrapper(self: Dispatcher, params: dict, **kwargs) -> dict:
        user_id = params.get("user_id")
        self._check_object(user_id, name="user_id")

        token = params.get("token")
        self._check_object(token, name="token")

        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        repository = self.repository
        repository.select_one(token=token, user_id=user_id)
        return func(self, params=params, **kwargs)

    return _wrapper


def checking_invitation(func: Callable) -> Callable:
    @functools.wraps(func)
    def _wrapper(self: Dispatcher, params: dict, **kwargs) -> dict:
        user_id = params.get("user_id")
        self._check_object(user_id, name="user_id")

        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        expected_users: list[int] = container.resolve(f"game.namespaces.{game_id}.users")

        if user_id not in expected_users:
            msg = f"Пользователь не зарегистрирован в игре {game_id}"
            raise AuthenticationException(msg)

        return func(self, params=params, **kwargs)

    return _wrapper


class Dispatcher:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    @property
    def repository(self) -> BaseRepository:
        return self._repository

    def dispatch(self, action: str, params: dict, auth_queue: str, channel: BlockingChannel) -> dict:
        method = getattr(self, f"_handle_{action}", None)
        if method is None:
            msg = f"Ошибка диспетчеризации, метод {action} не реализован"
            raise ValueError(msg)

        return method(params=params, auth_queue=auth_queue, channel=channel)

    def _handle_get_token(self, params: dict, auth_queue: str, channel: BlockingChannel) -> dict:
        user_id = params.get("user_id")
        self._check_object(user_id, name="user_id")

        payload = {"user_id": user_id, "action": "get_token"}
        channel.basic_publish(
            exchange="",
            routing_key=auth_queue,
            body=json.dumps(payload).encode("utf-8"),
        )
        return {"action": "get_token", "status": "expect to receive a token"}

    def _handle_save_token(self, params: dict, **kwargs) -> dict:
        token = params.get("token")
        self._check_object(token, name="token")

        user_id = params.get("user_id")
        self._check_object(user_id, name="user_id")

        self._repository.insert(token=token, user_id=user_id)
        return {"action": "save_token", "status": "ok", "user_id": user_id, "token": token}

    @token_required
    def _handle_register_game(self, params: dict, **kwargs) -> dict:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        objects_params = params.get("objects")
        self._check_object(objects_params, name="objects")

        user_ids = params.get("user_ids")
        self._check_object(user_ids, name="user_ids")

        game_objects = []
        for number, param in enumerate(objects_params, start=1):
            game_object = container.resolve("game.objects.create", params=param)
            container.resolve(
                "ioc.register",
                params={
                    "obj_name": f"game.namespaces.{game_id}.object_{number}",
                    "obj": lambda params: game_object,  # noqa
                },
            )
            data = game_object.data
            data["object_id"] = number
            game_objects.append(data)

        container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.namespaces.{game_id}.users",
                "obj": lambda params: user_ids,  # noqa
            },
        )

        return {"action": "register_game", "game_id": game_id, "objects": game_objects}

    @token_required
    @checking_invitation
    def _handle_start_game(self, params: dict, **kwargs) -> dict:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        queue = container.resolve("command.get_queue", params={"queue": Queue()}).execute()

        thread_command = container.resolve("command.to_thread", params={"queue": queue})
        thread_command.execute()

        container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.namespaces.{game_id}.tread",
                "obj": lambda params: thread_command.thread,  # noqa
            },
        )

        container.resolve(
            "ioc.register",
            params={"obj_name": f"game.namespaces.{game_id}.queue", "obj": lambda params: queue},  # noqa
        )
        return {"action": "start_game", "game_id": game_id}

    @token_required
    @checking_invitation
    def _handle_execute_command(self, params: dict, **kwargs) -> dict:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        object_id = params.get("object_id")
        self._check_object(object_id, name="object_id")

        command_name = params.get("command_name")
        self._check_object(command_name, name="command_name")

        thread: Thread = container.resolve(f"game.namespaces.{game_id}.tread")
        if not thread.is_alive():
            msg = "Игра не запущена или остановлена"
            raise ValueError(msg)

        game_object = container.resolve(f"game.namespaces.{game_id}.object_{object_id}")
        game_queue = container.resolve(f"game.namespaces.{game_id}.queue")
        interpret_command = container.resolve(
            "command.interpret",
            params={
                "ioc_container": container,
                "game_object": game_object,
                "game_queue": game_queue,
                "command_name": command_name,
            },
        )
        interpret_command.execute()
        return {"action": "execute_command", "game_id": game_id, "game_object": game_object.data}

    @staticmethod
    def _check_object(object_: Any, name: str) -> None:
        if object_ is None:
            msg = f"{name} обязательное поле"
            raise ValueError(msg)
