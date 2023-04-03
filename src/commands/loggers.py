from src.commands.base import BaseCommand
from src.logger.settings import logger


class ExceptionLoggingCommand(BaseCommand):
    def __init__(self, exception: Exception, *args, **kwargs) -> None:
        self._exception = exception

    def execute(self) -> None:
        msg = f"{type(self._exception).__name__}: {self._exception}"
        logger.exception(msg, exc_info=False)
