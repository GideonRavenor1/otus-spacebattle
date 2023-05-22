from src.game.commands.base import BaseCommand
from src.game.logger.settings import logger


class ExceptionLoggingCommand(BaseCommand):
    def __init__(self, *, exception: Exception, **kwargs) -> None:
        self._exception = exception

    def execute(self) -> None:
        msg = f"{type(self._exception).__name__}: {self._exception}"
        with self.lock:
            logger.exception(msg, exc_info=False)
