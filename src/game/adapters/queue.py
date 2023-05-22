from queue import Queue

from src.game.commands.base import BaseCommand
from src.game.exceptions import HardStop, SoftStop
from src.game.handlers import ExceptionHandler
from src.game.logger.settings import logger


class QueueAdapter:
    def __init__(self, queue: Queue) -> None:
        self._queue = queue
        self._can_work_calculation = lambda: True
        self._exception_handler = ExceptionHandler()

    def get(self) -> BaseCommand:
        return self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()

    def put(self, command: BaseCommand) -> None:
        self._queue.put(command)

    def stop_hard(self) -> None:
        self._can_work_calculation = lambda: False

    def stop_soft(self) -> None:
        self._can_work_calculation = lambda: not self._queue.empty()

    @property
    def can_work(self) -> bool:
        return self._can_work_calculation()

    def __call__(self, *args, **kwargs) -> None:
        while self.can_work:
            command = self._queue.get()
            try:
                command.execute()
            except SoftStop:
                with command.lock:
                    logger.info("Мягкая остановка очереди")
                self.stop_soft()
            except HardStop:
                with command.lock:
                    logger.info("Жесткая остановка очереди")
                self.stop_hard()
            except Exception as exception:
                self._exception_handler.handle(command, exception)

            self._queue.task_done()
