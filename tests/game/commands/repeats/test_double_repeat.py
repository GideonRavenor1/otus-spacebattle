import random
import uuid

import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import ReadPositionException, RepeatException
from src.game.vectors import Vector


def test_double_repeat_valid_params() -> None:
    """
    Проверяем, что команда повторяется и сдвигает объект с места
    """
    user_id = random.randint(1, 100)
    mock_obj = {"position": [12, 5], "velocity": [-7, 3], "user_id": user_id}
    mock_movable_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = command_container.resolve("command.move", params=move_params)

    repeat_params = {"command": command}
    repeat_command = command_container.resolve("command.second_repeat", params=repeat_params)

    repeat_command.execute()

    assert mock_movable_obj.get_position() == Vector(5, 8, mock_movable_obj.get_id())


def test_double_repeat_raise_exception() -> None:
    """
    Проверяем, что при повторных запусков команды в лог выводится сообщение об ошибке
    """
    user_id = random.randint(1, 100)
    object_id = str(uuid.uuid4())

    mock_obj = {"position": Vector(12, 5, object_id), "velocity": Vector(-7, 3, object_id)}

    class MovableImplementation:
        def get_position(self) -> Vector:
            raise ReadPositionException

        def set_position(self, vector: Vector) -> None:
            mock_obj["position"] = vector

        def get_velocity(self) -> Vector:
            return mock_obj["velocity"]

        def get_user_id(self) -> int:
            return user_id

    move_params = {"obj": MovableImplementation()}
    command = command_container.resolve("command.move", params=move_params)

    repeat_params = {"command": command}
    repeat_command = command_container.resolve("command.second_repeat", params=repeat_params)
    with pytest.raises(RepeatException):
        repeat_command.execute()
