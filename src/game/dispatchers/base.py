import functools
import json
from collections.abc import Callable
from queue import Queue
from threading import Thread
from typing import Any

from pika.adapters.blocking_connection import BlockingChannel

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import AuthenticationException
from src.game.handlers.state import CommandProcessor
from src.game.repositories.base import BaseRepository
from src.interpreter import CommandInterpreter


def token_required(func: Callable) -> Callable:
    @functools.wraps(func)
    def _wrapper(self: "Dispatcher", params: dict, **kwargs) -> dict:
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
    def _wrapper(self: "Dispatcher", params: dict, **kwargs) -> dict:
        user_id = params.get("user_id")
        self._check_object(user_id, name="user_id")

        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        expected_users: list[int] = game_container.resolve(f"game.namespaces.{game_id}.users")

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

        map_size = params.get("map_size")
        self._check_object(map_size, name="map_size")

        objects_params = params.get("objects")
        self._check_object(objects_params, name="objects")

        user_ids = params.get("user_ids")
        self._check_object(user_ids, name="user_ids")

        game_map = game_container.resolve("game.objects.create.map", params={"map_size": map_size})
        game_container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.namespaces.{game_id}.map",
                "obj": lambda params: game_map,  # noqa
            },
        )

        game_objects = []
        for param in objects_params:
            param["user_id"] = params.get("user_id")
            game_object = game_container.resolve("game.objects.create.object", params=param)
            game_container.resolve(
                "ioc.register",
                params={
                    "obj_name": f"game.namespaces.{game_id}.object_{game_object.id}",
                    "obj": lambda params: game_object,  # noqa
                },
            )
            data = game_object.data
            data["object_id"] = game_object.id
            game_objects.append(data)

            game_map.set_vector_position(game_object.id, param["x"], param["y"])

        game_container.resolve(
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

        queue = command_container.resolve("command.get_queue", params={"queue": Queue(), "game_id": game_id}).execute()
        command_processor = CommandProcessor(queue)
        thread_command = command_container.resolve("command.to_thread", params={"command_processor": command_processor})
        thread_command.execute()

        game_container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.namespaces.{game_id}.tread",
                "obj": lambda params: thread_command.thread,  # noqa
            },
        )

        game_container.resolve(
            "ioc.register",
            params={"obj_name": f"game.namespaces.{game_id}.queue", "obj": lambda params: queue},  # noqa
        )
        return {"action": "start_game", "game_id": game_id}

    @token_required
    @checking_invitation
    def _handle_add_game_object(self, params: dict, **kwargs) -> dict:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        object_params: dict = params.get("object_params")
        self._check_object(object_params, name="object_params")

        object_params["user_id"] = params.get("user_id")

        game_object = game_container.resolve("game.objects.create.object", params=object_params)
        game_container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.namespaces.{game_id}.object_{game_object.id}",
                "obj": lambda params: game_object,  # noqa
            },
        )
        return {"action": "add_game_object", "game_id": game_id, "object": game_object.data}

    @token_required
    @checking_invitation
    def _handle_execute_command(self, params: dict, **kwargs) -> dict:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        object_id = params.get("object_id")
        self._check_object(object_id, name="object_id")

        command_name = params.get("command_name")
        self._check_object(command_name, name="command_name")

        thread: Thread = game_container.resolve(f"game.namespaces.{game_id}.tread")
        if not thread.is_alive():
            msg = f"Игра {game_id} не запущена или остановлена"
            raise ValueError(msg)

        game_object = game_container.resolve(f"game.namespaces.{game_id}.object_{object_id}")
        if not game_object.is_alive():
            msg = f"Объект {game_object.get_id()} уничтожен"
            raise ValueError(msg)

        game_queue = game_container.resolve(f"game.namespaces.{game_id}.queue")
        interpreter = CommandInterpreter(
            ioc_container=command_container,
            game_object=game_object,
            game_queue=game_queue,
            command_name=command_name,
            user_id=params.get("user_id"),
        )
        interpreter.interpret()
        return {"action": "execute_command", "game_id": game_id, "game_object": game_object.data}

    @staticmethod
    def _check_object(object_: Any, name: str) -> None:
        if object_ is None:
            msg = f"{name} обязательное поле"
            raise ValueError(msg)
