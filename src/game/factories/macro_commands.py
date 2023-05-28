from typing import TypeVar

from src.game.commands import (
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    ForwardMacroCommand,
    MoveCommand,
    RotateCommand,
    ForwardWithRotateMacroCommand,
)
from src.game.factories.base import BaseCommandFactory
from src.game.interfaces import Movable, NeedsFuel, Rotatable

T_MNR = TypeVar("T_MNR", bound=Movable | NeedsFuel | Rotatable)
T_MN = TypeVar("T_MN", bound=Movable | NeedsFuel)


class ForwardMacroCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ForwardMacroCommand]:
        return ForwardMacroCommand

    def __call__(self, *, params: dict) -> ForwardMacroCommand:
        obj: T_MN | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект Movable | NeedsFuel")

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
        obj: T_MNR | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект Movable | NeedsFuel | Rotatable")

        macro_command = self.command()
        macro_command.add(command=CheckFuelCommand(obj=obj))
        macro_command.add(command=MoveCommand(obj=obj))
        macro_command.add(command=BurnFuelCommand(obj=obj))

        macro_command.add(command=CheckFuelCommand(obj=obj))
        macro_command.add(command=RotateCommand(obj=obj))
        macro_command.add(command=ChangeVelocityCommand(obj=obj))
        macro_command.add(command=BurnFuelCommand(obj=obj))
        return macro_command
