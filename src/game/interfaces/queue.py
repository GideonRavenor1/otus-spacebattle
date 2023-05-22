from typing import Protocol

from src.game.commands.base import BaseCommand


class IQueue(Protocol):
    def get(self) -> BaseCommand:
        ...

    def task_done(self) -> None:
        ...

    def put(self, command: BaseCommand) -> None:
        ...

    def stop_hard(self) -> None:
        ...

    def stop_soft(self) -> None:
        ...

    def can_work(self) -> bool:
        ...

    def __call__(self, *args, **kwargs) -> None:
        ...
