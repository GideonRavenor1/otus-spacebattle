from abc import ABC, abstractmethod
from typing import Optional

from src.exceptions import CommandException


class BaseCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class BaseMacroCommand(BaseCommand):
    def __init__(self, *, commands: Optional[list[BaseCommand]] = None, **kwargs) -> None:
        self._commands = [] if commands is None else commands

    def add(self, command: BaseCommand) -> None:
        self._commands.append(command)

    def remove(self, command: BaseCommand) -> None:
        self._commands.remove(command)

    def execute(self) -> None:
        for command in self._commands:
            try:
                command.execute()
            except Exception as ex:
                raise CommandException(str(ex)) from ex
