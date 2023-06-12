from typing import TypeVar

from src.game.commands import (
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    ForwardMacroCommand,
    MoveCommand,
    RotateCommand,
    ForwardWithRotateMacroCommand,
    CheckMapCollisionCommand,
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


class ForwardWithRotateMacroCommandFactory(BaseCommandFactory):
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


class ForwardAndCheckCollisionMacroCommandFactory(ForwardMacroCommandFactory):
    def __call__(self, *, params: dict) -> ForwardMacroCommand:
        macro_command = super().__call__(params=params)
        obj: T_MN = params.get("obj")

        game_id = params.get("game_id")
        if game_id is None:
            raise ValueError("Не указан game_id")

        ioc_container = params.get("ioc_container")
        if ioc_container is None:
            raise ValueError("Не указан ioc_container")

        macro_command.add(command=CheckMapCollisionCommand(obj=obj, game_id=game_id, ioc_container=ioc_container))
        return macro_command


class ForwardWithRotateAndCheckCollisionMacroCommandFactory(ForwardWithRotateMacroCommandFactory):
    def __call__(self, *, params: dict) -> ForwardWithRotateMacroCommand:
        macro_command = super().__call__(params=params)
        obj: T_MNR = params.get("obj")

        game_id = params.get("game_id")
        if game_id is None:
            raise ValueError("Не указан game_id")

        ioc_container = params.get("ioc_container")
        if ioc_container is None:
            raise ValueError("Не указан ioc_container")

        macro_command.add(command=CheckMapCollisionCommand(obj=obj, game_id=game_id, ioc_container=ioc_container))
        return macro_command
