from typing import TYPE_CHECKING

from queue import Queue
from threading import Thread

from src.game.adapters import QueueAdapter
from src.game.commands.base import BaseCommand
from src.game.interfaces import IQueue

if TYPE_CHECKING:
    from src.game.handlers.state import CommandProcessor


class QueueCommand(BaseCommand):
    adapter: type[QueueAdapter] = QueueAdapter

    def __init__(self, *, queue: Queue, game_id: str, **kwargs) -> None:
        self._queue = queue
        self._game_id = game_id

    def execute(self) -> IQueue:
        return QueueAdapter(queue=self._queue, game_id=self._game_id)


class ThreadCommand(BaseCommand):
    def __init__(self, *, command_processor: "CommandProcessor", **kwargs) -> None:
        self._command_processor = command_processor
        self._thread = Thread(target=self._command_processor)

    def execute(self) -> None:
        self._thread.start()

    @property
    def thread(self) -> Thread:
        return self._thread


class SoftStopCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        ...


class HardStopCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        ...


class MoveToCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        ...


class RunCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        ...
