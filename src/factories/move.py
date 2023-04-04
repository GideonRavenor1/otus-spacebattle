from typing import Optional

from src.commands import ChangeVelocityCommand, MoveCommand
from src.factories.base import BaseCommandFactory
from src.interfaces import Movable, VelocityChanger


class MoveCommandFactory(BaseCommandFactory):
    command = MoveCommand

    def create(self) -> MoveCommand:
        obj: Optional[Movable] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)


class ChangeVelocityCommandFactory(BaseCommandFactory):
    command = ChangeVelocityCommand

    def create(self) -> ChangeVelocityCommand:
        obj: Optional[VelocityChanger] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)
