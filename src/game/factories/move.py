from src.game.commands import ChangeVelocityCommand, MoveCommand
from src.game.factories.base import BaseCommandFactory
from src.game.interfaces import Movable, VelocityChanger


class MoveCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[MoveCommand]:
        return MoveCommand

    def __call__(self, *, params: dict) -> MoveCommand:
        obj: Movable | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект Movable")

        return self.command(obj=obj)


class ChangeVelocityCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[ChangeVelocityCommand]:
        return ChangeVelocityCommand

    def __call__(self, *, params: dict) -> ChangeVelocityCommand:
        obj: VelocityChanger | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект VelocityChanger")

        return self.command(obj=obj)
