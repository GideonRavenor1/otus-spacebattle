from typing import Protocol

from src.game.commands.base import BaseCommand


class IQueue(Protocol):
    def get(self) -> BaseCommand:
        ...

    def task_done(self) -> None:
        ...

    def put(self, command: BaseCommand) -> None:
        ...

    def is_empty(self) -> bool:
        ...

    def get_game_id(self) -> str:
        ...
