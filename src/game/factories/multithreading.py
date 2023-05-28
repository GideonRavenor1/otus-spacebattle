from queue import Queue
from typing import Optional

from src.game.commands import QueueCommand, ThreadCommand, SoftStopCommand, HardStopCommand
from src.game.factories.base import BaseCommandFactory
from src.game.interfaces import IQueue


class QueueCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[QueueCommand]:
        return QueueCommand

    def __call__(self, *, params: dict) -> QueueCommand:
        queue: Optional["Queue"] = params.get("queue")
        if queue is None:
            raise ValueError("Не указана очередь Queue")
        return self.command(queue=queue)


class ThreadCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ThreadCommand]:
        return ThreadCommand

    def __call__(self, *, params: dict) -> ThreadCommand:
        queue: Optional["IQueue"] = params.get("queue")
        if queue is None:
            raise ValueError("Не указана очередь IQueue")
        return self.command(queue=queue)


class SoftStopCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[SoftStopCommand]:
        return SoftStopCommand

    def __call__(self, *, params: dict) -> SoftStopCommand:
        return self.command()


class HardStopCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[HardStopCommand]:
        return HardStopCommand

    def __call__(self, *, params: dict) -> HardStopCommand:
        return self.command()
