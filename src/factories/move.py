from typing import Optional

from src.commands import ChangeVelocityCommand, MoveCommand
from src.factories.base import BaseCommandFactory
from src.interfaces import Movable, VelocityChanger


class MoveCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[MoveCommand]:
        return MoveCommand

    def __call__(self, *, params: dict) -> MoveCommand:
        obj: Optional[Movable] = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)


class ChangeVelocityCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ChangeVelocityCommand]:
        return ChangeVelocityCommand

    def __call__(self, *, params: dict) -> ChangeVelocityCommand:
        obj: Optional[VelocityChanger] = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)
