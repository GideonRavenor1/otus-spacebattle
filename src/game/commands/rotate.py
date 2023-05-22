from src.game.commands.base import BaseCommand
from src.game.interfaces.movements import Rotatable


class RotateCommand(BaseCommand):
    def __init__(self, *, obj: Rotatable, **kwargs) -> None:
        self._obj = obj

    def execute(self) -> None:
        self._obj.set_direction(
            self._obj.get_direction() + self._obj.get_angular_velocity() % self._obj.get_direction_number(),
        )
