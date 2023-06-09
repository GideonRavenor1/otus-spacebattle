from src.game.commands.base import BaseCommand
from src.game.exceptions import SetPositionException
from src.game.interfaces import Movable, VelocityChanger
from src.game.vectors import Vector


class MoveCommand(BaseCommand):
    def __init__(self, *, obj: Movable, **kwargs) -> None:
        self._obj = obj

    def execute(self) -> None:
        old_position = self._obj.get_position()
        new_position = self._obj.get_position() + self._obj.get_velocity()
        if old_position == new_position:
            raise SetPositionException("Объект не сдвинулся с места")
        self._obj.set_position(new_position)


class ChangeVelocityCommand(BaseCommand):
    def __init__(self, obj: VelocityChanger) -> None:
        self._obj = obj

    def execute(self) -> None:
        current_velocity = self._obj.get_velocity()
        delta_direction = self._obj.get_angular_velocity()
        new_velocity = Vector(
            current_velocity.y * delta_direction,
            -current_velocity.x * delta_direction,
            object_id=self._obj.get_id(),
        )
        self._obj.set_velocity(new_velocity)
