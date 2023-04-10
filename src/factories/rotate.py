from typing import Optional

from src.commands import RotateCommand
from src.factories.base import BaseCommandFactory
from src.interfaces.movements import Rotatable


class RotateCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[RotateCommand]:
        return RotateCommand

    def __call__(self, *, params: dict) -> RotateCommand:
        obj: Optional[Rotatable] = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)
