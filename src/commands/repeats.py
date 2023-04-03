from src.commands.base import BaseCommand
from src.exceptions import RepeatException


class FirstRepeatCommand(BaseCommand):
    def __init__(self, command: BaseCommand, *args, **kwargs) -> None:
        self._command = command

    def execute(self) -> None:
        try:
            self._command.execute()
        except Exception as ex:
            raise RepeatException(str(ex))


class SecondRepeatCommand(FirstRepeatCommand):
    ...
