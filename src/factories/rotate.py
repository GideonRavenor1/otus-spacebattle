from typing import Optional

from src.commands import RotateCommand
from src.factories.base import BaseCommandFactory
from src.interfaces.movements import Rotatable


class RotateCommandFactory(BaseCommandFactory):
    command = RotateCommand

    def create(self) -> RotateCommand:
        obj: Optional[Rotatable] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")

        return self.command(obj=obj)
