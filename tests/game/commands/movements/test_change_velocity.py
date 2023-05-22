import pytest

from src.game.dependencies import container
from src.game.exceptions import ReadVelocityException, SetVelocityException
from src.game.vectors import Vector


def test_change_velocity_valid_params() -> None:
    """
    Проверка модификации вектора мгновенной скорости при повороте.
    """

    mock_obj = {"velocity": [-7, 3], "direction": 100, "angular_velocity": 30, "direction_number": 360}

    obj = container.resolve("game.objects.create", params=mock_obj)
    params = {"obj": obj}
    container.resolve("command.change_velocity", params=params).execute()

    assert obj.get_velocity() == Vector(90, 210)


def test_change_velocity_impossible_set_velocity() -> None:
    """
    Проверка модификации вектора мгновенной скорости при повороте, если невозможно изменить мгновенную скорость.
    """

    mock_obj = {"velocity": Vector(-7, 3), "direction": 100, "angular_velocity": 30, "direction_number": 360}

    class ChangeVelocityImplementation:
        def get_velocity(self) -> Vector:
            return mock_obj["velocity"]

        def set_velocity(self, vector: Vector) -> None:
            raise SetVelocityException

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

    params = {"obj": ChangeVelocityImplementation()}
    with pytest.raises(SetVelocityException):
        container.resolve("command.change_velocity", params=params).execute()


def test_change_velocity_impossible_read_velocity() -> None:
    """
    Проверка модификации вектора мгновенной скорости при повороте, если объект невозможен прочитать мгновенную скорость.
    """

    mock_obj = {"velocity": Vector(-7, 3), "direction": 100, "angular_velocity": 30, "direction_number": 360}

    class ChangeVelocityImplementation:
        def get_velocity(self) -> Vector:
            raise ReadVelocityException

        def set_velocity(self, vector: Vector) -> None:
            mock_obj["velocity"] = vector

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

    params = {"obj": ChangeVelocityImplementation()}
    with pytest.raises(ReadVelocityException):
        container.resolve("command.change_velocity", params=params).execute()


def test_change_velocity_impossible_read_angular_velocity() -> None:
    """
    Проверка модификации вектора мгновенной скорости при повороте, если невозможно прочитать угловую скорость
    """

    mock_obj = {"velocity": Vector(-7, 3), "direction": 100, "angular_velocity": 30, "direction_number": 360}

    class ChangeVelocityImplementation:
        def get_velocity(self) -> Vector:
            raise ReadVelocityException

        def set_velocity(self, vector: Vector) -> None:
            mock_obj["velocity"] = vector

        def get_angular_velocity(self) -> int:
            return mock_obj["angular_velocity"]

    params = {"obj": ChangeVelocityImplementation()}
    with pytest.raises(ReadVelocityException):
        container.resolve("command.change_velocity", params=params).execute()