from typing import Optional, TypeVar, Union

from src.commands import BaseMacroCommand, BurnFuelCommand, CheckFuelCommand, MoveCommand
from src.factories.base import BaseMacroCommandFactory
from src.interfaces import Movable, NeedsFuel

T_MN = TypeVar("T_MN", bound=Union[Movable, NeedsFuel])


class ForwardMacroCommandFactory(BaseMacroCommandFactory):
    def __init__(self, obj: T_MN, macro_command: Optional[BaseMacroCommand] = None) -> None:
        super().__init__(macro_command)
        self._obj = obj

    def create(self) -> BaseMacroCommand:
        self._macro_command.add(CheckFuelCommand(obj=self._obj))
        self._macro_command.add(MoveCommand(obj=self._obj))
        self._macro_command.add(BurnFuelCommand(obj=self._obj))
        return self._macro_command
