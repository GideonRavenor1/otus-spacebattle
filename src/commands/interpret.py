from typing import TYPE_CHECKING

from src.commands import BaseCommand


if TYPE_CHECKING:
    from src.dependencies import IoCContainer
    from src.game_object import GameObject
    from src.adapters import QueueAdapter


class InterpretCommand(BaseCommand):
    def __init__(
        self,
        *,
        ioc_container: "IoCContainer",
        command_name: str,
        game_object: "GameObject",
        game_queue: "QueueAdapter",
    ) -> None:
        self._ioc_container = ioc_container
        self._command_name = command_name
        self._game_object = game_object
        self._game_queue = game_queue

    def execute(self) -> None:
        params = {"obj": self._game_object}
        command = self._ioc_container.resolve(self._command_name, params=params)
        self._game_queue.put(command)
