from queue import Queue
from threading import Thread
from typing import Any

from src.dependencies import container


class Dispatcher:
    def dispatch(self, action: str, params: dict) -> None:
        method = getattr(self, f"_handle_{action}", None)
        if method is None:
            msg = f"Ошибка диспетчеризации, метод {action} не реализован"
            raise ValueError(msg)

        method(params=params)

    def _handle_register_game(self, params: dict) -> None:
        game_id = params.get("game_id")
        self._check_object(game_id, name="game_id")

        objects_params = params.get("objects")
        self._check_object(objects_params, name="objects")

        for number, param in enumerate(objects_params, start=1):
            game_object = container.resolve("game.objects.create", params=param)
            container.resolve(
                "ioc.register",
                params={
                    "obj_name": f"game.namespaces.{game_id}.object_{number}",
                    "obj": lambda params: game_object,  # noqa
                },
            )

    def _handle_start_game(self, params: dict) -> None:
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

    def _handle_execute_command(self, params: dict) -> None:
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

    @staticmethod
    def _check_object(object_: Any, name: str) -> None:
        if object_ is None:
            msg = f"{name} обязательное поле"
            raise ValueError(msg)
