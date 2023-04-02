from src.commands.base import BaseCommand
from src.logger.settings import logger


class ExceptionLoggingCommand(BaseCommand):
    def __init__(self, exception: Exception) -> None:
        self._exception = exception

    def execute(self) -> None:
        logger.exception(f"{type(self._exception).__name__}: {self._exception}", exc_info=False)