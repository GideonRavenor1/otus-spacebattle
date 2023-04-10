import pytest

from src.dependencies import container
from src.exceptions import ReadPositionException, RepeatException
from src.vectors import Vector
from tests.utils import get_game_object


def test_double_repeat_valid_params() -> None:
    """
    Проверяем, что команда повторяется и сдвигает объект с места
    """

    mock_obj = {"position": Vector(12, 5), "velocity": Vector(-7, 3)}
    mock_movable_obj = get_game_object(data=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = container["move"](params=move_params)

    repeat_params = {"command": command}
    repeat_command = container["second_repeat"](params=repeat_params)

    repeat_command.execute()

    assert mock_movable_obj.get_position() == Vector(5, 8)


def test_double_repeat_raise_exception() -> None:
    """
    Проверяем, что при повторных запусков команды в лог выводится сообщение об ошибке
    """

    mock_obj = {"position": Vector(12, 5), "velocity": Vector(-7, 3)}

    class MovableImplementation:
        def get_position(self) -> Vector:
            raise ReadPositionException

        def set_position(self, vector: Vector) -> None:
            mock_obj["position"] = vector

        def get_velocity(self) -> Vector:
            return mock_obj["velocity"]

    move_params = {"obj": MovableImplementation()}
    command = container["move"](params=move_params)

    repeat_params = {"command": command}
    repeat_command = container["second_repeat"](params=repeat_params)
    with pytest.raises(RepeatException):
        repeat_command.execute()
