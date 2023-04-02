from abc import ABC, abstractmethod
from typing import Optional

from src.commands import BaseMacroCommand


class BaseMacroCommandFactory(ABC):
    def __init__(self, macro_command: Optional[BaseMacroCommand] = None) -> None:
        self._macro_command = BaseMacroCommand() if macro_command is None else macro_command

    @abstractmethod
    def create(self) -> BaseMacroCommand:
        raise NotImplementedError
