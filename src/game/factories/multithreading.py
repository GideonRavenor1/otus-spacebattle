from queue import Queue
from typing import Optional, TYPE_CHECKING

from src.game.commands import (
    QueueCommand,
    ThreadCommand,
    SoftStopCommand,
    HardStopCommand,
    MoveToCommand,
    RunCommand,
)
from src.game.factories.base import BaseCommandFactory

if TYPE_CHECKING:
    from src.game.handlers.state import CommandProcessor


class QueueCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[QueueCommand]:
        return QueueCommand

    def __call__(self, *, params: dict) -> QueueCommand:
        queue: Optional["Queue"] = params.get("queue")
        game_id = params.get("game_id")

        if queue is None:
            raise ValueError("Не указана очередь Queue")

        if game_id is None:
            raise ValueError("Не указан id игры")

        return self.command(queue=queue, game_id=game_id)


class ThreadCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ThreadCommand]:
        return ThreadCommand

    def __call__(self, *, params: dict) -> ThreadCommand:
        command_processor: Optional["CommandProcessor"] = params.get("command_processor")
        if command_processor is None:
            raise ValueError("Не указана процессор Queue")
        return self.command(command_processor=command_processor)


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


class MoveToCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[MoveToCommand]:
        return MoveToCommand

    def __call__(self, *, params: dict) -> MoveToCommand:
        return self.command()


class RunCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[RunCommand]:
        return RunCommand

    def __call__(self, *, params: dict) -> RunCommand:
        return self.command()
