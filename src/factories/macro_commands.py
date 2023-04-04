from typing import Optional, TypeVar, Union

from src.commands import (
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    ForwardMacroCommand,
    MoveCommand,
    RotateCommand,
    ForwardWithRotateMacroCommand,
)
from src.factories.base import BaseCommandFactory
from src.interfaces import Movable, NeedsFuel, Rotatable

T_MNR = TypeVar("T_MNR", bound=Union[Movable, NeedsFuel, Rotatable])
T_MN = TypeVar("T_MN", bound=Union[Movable, NeedsFuel])


class ForwardMacroCommandFactory(BaseCommandFactory):
    command = ForwardMacroCommand

    def create(self) -> ForwardMacroCommand:
        obj: Optional[T_MN] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        self.command = self.command()
        self.command.add(command=CheckFuelCommand(obj=obj))
        self.command.add(command=MoveCommand(obj=obj))
        self.command.add(command=BurnFuelCommand(obj=obj))
        return self.command


class ForwardWithRotateCommandFactory(BaseCommandFactory):
    command = ForwardWithRotateMacroCommand

    def create(self) -> ForwardWithRotateMacroCommand:
        obj: Optional[T_MNR] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        self.command = self.command()
        self.command.add(command=CheckFuelCommand(obj=obj))
        self.command.add(command=MoveCommand(obj=obj))
        self.command.add(command=BurnFuelCommand(obj=obj))

        self.command.add(command=CheckFuelCommand(obj=obj))
        self.command.add(command=RotateCommand(obj=obj))
        self.command.add(command=ChangeVelocityCommand(obj=obj))
        self.command.add(command=BurnFuelCommand(obj=obj))
        return self.command
