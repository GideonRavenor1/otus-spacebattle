from typing import Optional

from src.commands import FirstRepeatCommand
from src.commands.base import BaseCommand
from src.factories.base import BaseCommandFactory


class FirstRepeatCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[FirstRepeatCommand]:
        return FirstRepeatCommand

    def create(self, *, params: dict) -> FirstRepeatCommand:
        command: Optional[BaseCommand] = params.get("command")
        if command is None:
            raise ValueError("Не указана команда")
        return self.command(command=command)


class SecondRepeatCommandFactory(FirstRepeatCommandFactory):
    ...
