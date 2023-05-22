from src.game.commands.base import BaseCommand
from src.game.exceptions import RepeatException


class FirstRepeatCommand(BaseCommand):
    def __init__(self, *, command: BaseCommand, **kwargs) -> None:
        self._command = command

    def execute(self) -> None:
        try:
            self._command.execute()
        except Exception as ex:
            msg = f"{type(ex).__name__}, {ex!s}"
            raise RepeatException(msg)


class SecondRepeatCommand(FirstRepeatCommand):
    ...
