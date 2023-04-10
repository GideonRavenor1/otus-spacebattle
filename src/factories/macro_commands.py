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
    @property
    def command(self) -> type[ForwardMacroCommand]:
        return ForwardMacroCommand

    def __call__(self, *, params: dict) -> ForwardMacroCommand:
        obj: Optional[T_MN] = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        macro_command = self.command()
        macro_command.add(command=CheckFuelCommand(obj=obj))
        macro_command.add(command=MoveCommand(obj=obj))
        macro_command.add(command=BurnFuelCommand(obj=obj))
        return macro_command


class ForwardWithRotateCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ForwardWithRotateMacroCommand]:
        return ForwardWithRotateMacroCommand

    def __call__(self, *, params: dict) -> ForwardWithRotateMacroCommand:
        obj: Optional[T_MNR] = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        macro_command = self.command()
        macro_command.add(command=CheckFuelCommand(obj=obj))
        macro_command.add(command=MoveCommand(obj=obj))
        macro_command.add(command=BurnFuelCommand(obj=obj))

        macro_command.add(command=CheckFuelCommand(obj=obj))
        macro_command.add(command=RotateCommand(obj=obj))
        macro_command.add(command=ChangeVelocityCommand(obj=obj))
        macro_command.add(command=BurnFuelCommand(obj=obj))
        return macro_command
