from typing import Optional

from src.commands import FirstRepeatCommand
from src.commands.base import BaseCommand
from src.factories.base import BaseCommandFactory


class FirstRepeatCommandFactory(BaseCommandFactory):
    command = FirstRepeatCommand

    def create(self) -> BaseCommand:
        command: Optional[BaseCommand] = self._params.get("command")
        if command is None:
            raise ValueError("Не указана команда")
        return self.command(command=command)


class SecondRepeatCommandFactory(FirstRepeatCommandFactory):
    ...
