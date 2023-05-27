from typing import Any, Optional, TYPE_CHECKING

from src.game.commands import InterpretCommand
from src.game.factories.base import BaseCommandFactory

if TYPE_CHECKING:
    from src.game.dependencies import IoCContainer
    from src.game.game_object import GameObject
    from src.game.adapters import QueueAdapter


class InterpretCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[InterpretCommand]:
        return InterpretCommand

    def __call__(self, *, params: dict) -> InterpretCommand:
        ioc_container: Optional["IoCContainer"] = params.get("ioc_container")
        self._check_obj(obj=ioc_container, name="ioc_container")

        command_name: str | None = params.get("command_name")
        self._check_obj(obj=command_name, name="command_name")

        game_object: Optional["GameObject"] = params.get("game_object")
        self._check_obj(obj=game_object, name="game_object")

        game_queue: Optional["QueueAdapter"] = params.get("game_queue")
        self._check_obj(obj=game_queue, name="game_queue")

        return self.command(
            ioc_container=ioc_container,
            command_name=command_name,
            game_object=game_object,
            game_queue=game_queue,
        )

    @staticmethod
    def _check_obj(obj: Any, name: str) -> None:
        if obj is None:
            msg = f"Не указан объект {name}"
            raise ValueError(msg)
