import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import ReadDirectionException, RepeatException
from src.game.vectors import Vector


def test_repeat_valid_params() -> None:
    """
    Проверяем, что команда повторяется и сдвигает объект с места
    """

    mock_obj = {"direction": 250, "angular_velocity": 30, "direction_number": 360}
    mock_rotate_obj = game_container.resolve("game.objects.create", params=mock_obj)
    rotate_params = {"obj": mock_rotate_obj}
    command = command_container.resolve("command.rotate", params=rotate_params)

    repeat_params = {"command": command}
    repeat_command = command_container.resolve("command.first_repeat", params=repeat_params)
    repeat_command.execute()

    assert mock_rotate_obj.get_direction() == 280


def test_repeat_raise_exception() -> None:
    """
    Проверяем, что при повторных запусков команды в лог выводится сообщение об ошибке
    """

    mock_obj = {"position": Vector(12, 5), "velocity": Vector(-7, 3)}

    class RotatableImplementation:
        def get_direction(self) -> int:
            raise ReadDirectionException

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

        def get_direction_number(self) -> int:
            return mock_obj["direction_number"]

        def set_direction(self, value: int) -> None:
            mock_obj["direction"] = value

    rotate_params = {"obj": RotatableImplementation()}
    command = command_container.resolve("command.rotate", params=rotate_params)

    repeat_params = {"command": command}
    repeat_command = command_container.resolve("command.first_repeat", params=repeat_params)
    with pytest.raises(RepeatException):
        repeat_command.execute()
