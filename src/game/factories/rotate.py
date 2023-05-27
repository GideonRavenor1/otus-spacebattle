from src.game.commands import RotateCommand
from src.game.factories.base import BaseCommandFactory
from src.game.interfaces.movements import Rotatable


class RotateCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[RotateCommand]:
        return RotateCommand

    def __call__(self, *, params: dict) -> RotateCommand:
        obj: Rotatable | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)
