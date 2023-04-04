from typing import Optional

from src.commands import ExceptionLoggingCommand

from src.factories.base import BaseCommandFactory


class ExceptionLoggingCommandFactory(BaseCommandFactory):
    command = ExceptionLoggingCommand

    def create(self) -> ExceptionLoggingCommand:
        exception: Optional[Exception] = self._params.get("exception")
        if exception is None:
            raise ValueError("Не указано исключение")
        return self.command(exception=exception)
