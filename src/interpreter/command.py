from typing import TYPE_CHECKING

from src.game.exceptions import PermissionException
from src.interpreter.base import BaseInterpreter

if TYPE_CHECKING:
    from src.game.dependencies.base import IoCContainer
    from src.game.game_object import GameObject
    from src.game.adapters import QueueAdapter


class CommandInterpreter(BaseInterpreter):
    def __init__(
        self,
        *,
        ioc_container: "IoCContainer",
        command_name: str,
        game_object: "GameObject",
        game_queue: "QueueAdapter",
        user_id: int,
    ) -> None:
        if user_id != game_object.get_user_id():
            raise PermissionException("Нельзя использовать команду для объектов другого пользователя")
        self._ioc_container = ioc_container
        self._command_name = command_name
        self._game_object = game_object
        self._game_queue = game_queue

    def interpret(self) -> None:
        params = {"obj": self._game_object, "ioc_container": self._ioc_container}
        command = self._ioc_container.resolve(self._command_name, params=params)
        self._game_queue.put(command)
