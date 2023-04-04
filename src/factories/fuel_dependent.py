from typing import Optional

from src.commands import BurnFuelCommand, CheckFuelCommand
from src.factories.base import BaseCommandFactory
from src.interfaces import NeedsFuel


class CheckFuelCommandFactory(BaseCommandFactory):
    command = CheckFuelCommand

    def create(self) -> CheckFuelCommand:
        obj: Optional[NeedsFuel] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")
        return self.command(obj=obj)


class BurnFuelCommandFactory(BaseCommandFactory):
    command = BurnFuelCommand

    def create(self) -> BurnFuelCommand:
        obj: Optional[NeedsFuel] = self._params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")
        return self.command(obj=obj)
