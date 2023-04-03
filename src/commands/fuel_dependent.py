from src.commands.base import BaseCommand
from src.exceptions import NoFuelException
from src.interfaces import NeedsFuel


class CheckFuelCommand(BaseCommand):
    def __init__(self, *, obj: NeedsFuel, **kwargs) -> None:
        self._obj = obj

    def execute(self) -> None:
        if self._obj.get_fuel_level() - self._obj.get_required_fuel_level() < 0:
            raise NoFuelException("Недостаточно топлива")


class BurnFuelCommand(BaseCommand):
    def __init__(self, obj: NeedsFuel) -> None:
        self._obj = obj

    def execute(self) -> None:
        self._obj.set_fuel_level(self._obj.get_fuel_level() - self._obj.get_required_fuel_level())
