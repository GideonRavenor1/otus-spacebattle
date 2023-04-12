from typing import Optional, TypeVar, Union

from src.commands import (
    BaseMacroCommand,
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    MoveCommand,
    RotateCommand,
    ForwardWithRotateMacroCommand,
)
from src.factories import BaseMacroCommandFactory
from src.interfaces import Movable, NeedsFuel, Rotatable

T_MNR = TypeVar("T_MNR", bound=Union[Movable, NeedsFuel, Rotatable])


class ForwardWithRotateCommandFactory(BaseMacroCommandFactory):
    def __init__(
        self,
        *,
        obj: T_MNR,
        macro_command: Optional[type[BaseMacroCommand]] = ForwardWithRotateMacroCommand,
        **kwargs,
    ) -> None:
        super().__init__(macro_command=macro_command, **kwargs)
        self._obj = obj

    def create(self) -> BaseMacroCommand:
        self._macro_command.add(command=CheckFuelCommand(obj=self._obj))
        self._macro_command.add(command=MoveCommand(obj=self._obj))
        self._macro_command.add(command=BurnFuelCommand(obj=self._obj))

        self._macro_command.add(command=CheckFuelCommand(obj=self._obj))
        self._macro_command.add(command=RotateCommand(obj=self._obj))
        self._macro_command.add(command=ChangeVelocityCommand(obj=self._obj))
        self._macro_command.add(command=BurnFuelCommand(obj=self._obj))
        return self._macro_command
