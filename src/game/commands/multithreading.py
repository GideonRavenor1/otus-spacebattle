from queue import Queue
from threading import Thread

from src.game.adapters import QueueAdapter
from src.game.commands.base import BaseCommand
from src.game.exceptions import HardStop, SoftStop
from src.game.interfaces import IQueue


class QueueCommand(BaseCommand):
    adapter: type[QueueAdapter] = QueueAdapter

    def __init__(self, *, queue: Queue, **kwargs) -> None:
        self._queue = queue

    def execute(self) -> IQueue:
        return QueueAdapter(queue=self._queue)


class ThreadCommand(BaseCommand):
    def __init__(self, *, queue: IQueue, **kwargs) -> None:
        self._queue = queue
        self._thread = Thread(target=queue)

    def execute(self) -> None:
        self._thread.start()

    @property
    def thread(self) -> Thread:
        return self._thread


class SoftStopCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        raise SoftStop("Мягкая остановка очереди")


class HardStopCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> None:
        raise HardStop("Жесткая остановка очереди")
