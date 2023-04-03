from abc import ABC, abstractmethod
from typing import Optional

from src.commands import BaseMacroCommand


class BaseMacroCommandFactory(ABC):
    def __init__(
        self,
        *,
        macro_command: Optional[type[BaseMacroCommand]] = BaseMacroCommand,
        **kwargs,
    ) -> None:
        self._macro_command = macro_command()

    @abstractmethod
    def create(self) -> BaseMacroCommand:
        raise NotImplementedError
