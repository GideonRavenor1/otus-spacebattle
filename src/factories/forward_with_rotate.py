from typing import Optional, TypeVar, Union

from src.commands import (
    BaseMacroCommand,
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    MoveCommand,
    RotateCommand,
)
from src.factories import BaseMacroCommandFactory
from src.interfaces import Movable, NeedsFuel, Rotatable

T_MNR = TypeVar("T_MNR", bound=Union[Movable, NeedsFuel, Rotatable])


class ForwardWithRotateCommandFactory(BaseMacroCommandFactory):
    def __init__(self, obj: T_MNR, macro_command: Optional[BaseMacroCommand] = None) -> None:
        super().__init__(macro_command)
        self._obj = obj

    def create(self) -> BaseMacroCommand:
        self._macro_command.add(CheckFuelCommand(obj=self._obj))
        self._macro_command.add(MoveCommand(obj=self._obj))
        self._macro_command.add(BurnFuelCommand(obj=self._obj))

        self._macro_command.add(CheckFuelCommand(obj=self._obj))
        self._macro_command.add(RotateCommand(obj=self._obj))
        self._macro_command.add(ChangeVelocityCommand(obj=self._obj))
        self._macro_command.add(BurnFuelCommand(obj=self._obj))
        return self._macro_command
