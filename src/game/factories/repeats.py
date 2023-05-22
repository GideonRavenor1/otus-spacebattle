from typing import Optional

from src.game.commands import FirstRepeatCommand
from src.game.commands.base import BaseCommand
from src.game.factories.base import BaseCommandFactory


class FirstRepeatCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[FirstRepeatCommand]:
        return FirstRepeatCommand

    def __call__(self, *, params: dict) -> FirstRepeatCommand:
        command: Optional[BaseCommand] = params.get("command")
        if command is None:
            raise ValueError("Не указана команда")
        return self.command(command=command)


class SecondRepeatCommandFactory(FirstRepeatCommandFactory):
    ...
