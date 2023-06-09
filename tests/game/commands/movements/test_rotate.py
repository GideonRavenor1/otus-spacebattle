import random

import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import (
    RaedDirectionNumberException,
    ReadAngularVelocityException,
    ReadDirectionException,
    SetDirectionException,
)


@pytest.mark.parametrize(
    ("direction", "angular_velocity", "direction_number", "expected"),
    [(270, 30, 360, 300), (200, 0, 360, 200)],
)
def test_rotate_valid_param(direction: int, angular_velocity: int, direction_number: int, expected: int) -> None:
    """
    Положительные тесты, включающую нулевую угловую скорость
    """
    user_id = random.randint(1, 100)
    mock_obj = {
        "direction": direction,
        "angular_velocity": angular_velocity,
        "direction_number": direction_number,
        "user_id": user_id,
    }

    mock_rotate = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_rotate}
    command_container.resolve("command.rotate", params=params).execute()

    assert mock_rotate.get_direction() == expected


def test_rotate_impossible_read_direction() -> None:
    """
    Попытка повернуть объект, у которого невозможно прочитать текущее направление в пространстве, приводит к ошибке
    """
    user_id = random.randint(1, 100)
    mock_obj = {"direction": 100, "angular_velocity": 30, "direction_number": 360}

    class RotatableImplementation:
        def get_direction(self) -> int:
            raise ReadDirectionException

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

        def get_direction_number(self) -> int:
            return mock_obj["direction_number"]

        def set_direction(self, value: int) -> None:
            mock_obj["direction"] = value

        def get_user_id(self) -> int:
            return user_id

    params = {"obj": RotatableImplementation()}
    with pytest.raises(ReadDirectionException):
        command_container.resolve("command.rotate", params=params).execute()


def test_rotate_impossible_read_angular_velocity() -> None:
    """
    Попытка повернуть объект, у которого невозможно прочитать угловую скорость, приводит к ошибке
    """
    user_id = random.randint(1, 100)
    mock_obj = {"direction": 100, "angular_velocity": 30, "direction_number": 360}

    class RotatableImplementation:
        def get_direction(self) -> int:
            return mock_obj["direction"]

        def get_angular_velocity(self) -> int:
            raise ReadAngularVelocityException

        def get_direction_number(self) -> int:
            return mock_obj["direction_number"]

        def set_direction(self, value: int) -> None:
            mock_obj["direction"] = value

        def get_user_id(self) -> int:
            return user_id

    params = {"obj": RotatableImplementation()}
    with pytest.raises(ReadAngularVelocityException):
        command_container.resolve("command.rotate", params=params).execute()


def test_rotate_impossible_set_direction() -> None:
    """
    Попытка повернуть объект, у которого невозможно изменить текущее направление в пространстве, приводит к ошибке
    """
    user_id = random.randint(1, 100)
    mock_obj = {"direction": 100, "angular_velocity": 30, "direction_number": 360}

    class RotatableImplementation:
        def get_direction(self) -> int:
            return mock_obj["direction"]

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

        def get_direction_number(self) -> int:
            return mock_obj["direction_number"]

        def set_direction(self, value: int) -> None:
            raise SetDirectionException

        def get_user_id(self) -> int:
            return user_id

    params = {"obj": RotatableImplementation()}
    with pytest.raises(SetDirectionException):
        command_container.resolve("command.rotate", params=params).execute()


def test_rotate_impossible_read_direction_number() -> None:
    """
    Попытка повернуть объект, у которого невозможно прочитать номер направления, приводит к ошибке
    """
    user_id = random.randint(1, 100)
    mock_obj = {"direction": 100, "angular_velocity": 30, "direction_number": 360}

    class RotatableImplementation:
        def get_direction(self) -> int:
            return mock_obj["direction"]

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

        def get_direction_number(self) -> int:
            raise RaedDirectionNumberException

        def set_direction(self, value: int) -> None:
            mock_obj["direction_number"] = value

        def get_user_id(self) -> int:
            return user_id

    params = {"obj": RotatableImplementation()}
    with pytest.raises(RaedDirectionNumberException):
        command_container.resolve("command.rotate", params=params).execute()
