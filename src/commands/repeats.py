from src.commands.base import BaseCommand
from src.exceptions import RepeatException


class RepeatCommand(BaseCommand):
    def __init__(self, command: BaseCommand) -> None:
        self._command = command

    def execute(self) -> None:
        try:
            self._command.execute()
        except Exception as ex:
            raise RepeatException(str(ex))


class DoubleRepeatCommand(BaseCommand):
    MAX_RETRY = 2

    def __init__(self, command: BaseCommand) -> None:
        self._command = command

    def execute(self) -> None:
        exception = None
        for _ in range(self.MAX_RETRY):
            try:
                self._command.execute()
                return
            except Exception as ex:
                exception = ex
                continue
        raise RepeatException(str(exception))
