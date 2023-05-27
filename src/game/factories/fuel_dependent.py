from src.game.commands import BurnFuelCommand, CheckFuelCommand
from src.game.factories.base import BaseCommandFactory
from src.game.interfaces import NeedsFuel


class CheckFuelCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[CheckFuelCommand]:
        return CheckFuelCommand

    def __call__(self, *, params: dict) -> CheckFuelCommand:
        obj: NeedsFuel | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")
        return self.command(obj=obj)


class BurnFuelCommandFactory(BaseCommandFactory):
    @property
    def command(self) -> type[BurnFuelCommand]:
        return BurnFuelCommand

    def __call__(self, *, params: dict) -> BurnFuelCommand:
        obj: NeedsFuel | None = params.get("obj")
        if obj is None:
            raise ValueError("Не указан объект")
        return self.command(obj=obj)
