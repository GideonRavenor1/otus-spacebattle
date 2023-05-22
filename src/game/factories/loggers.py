from typing import Optional

from src.game.commands import ExceptionLoggingCommand

from src.game.factories.base import BaseCommandFactory


class ExceptionLoggingCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ExceptionLoggingCommand]:
        return ExceptionLoggingCommand

    def __call__(self, *, params: dict) -> ExceptionLoggingCommand:
        exception: Optional[Exception] = params.get("exception")
        if exception is None:
            raise ValueError("Не указано исключение")
        return self.command(exception=exception)
