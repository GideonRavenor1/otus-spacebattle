from queue import Queue

from src.game.commands.base import BaseCommand
from src.game.handlers.exception import ExceptionHandler
from src.game.managers.base import BaseManager


class QueueManager(BaseManager):
    def __init__(self, *, commands: list[BaseCommand], **kwargs) -> None:
        self._queue = Queue()
        self._exception_handler = ExceptionHandler()

        for command in commands:
            self._queue.put(command)

    def run(self) -> None:
        while not self._queue.empty():
            command = self._queue.get()
            try:
                command.execute()
            except Exception as exception:
                self._exception_handler.handle(command, exception)
