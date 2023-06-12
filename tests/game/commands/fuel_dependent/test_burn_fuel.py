import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import ReadFuelLevelException, ReadRequiredFuelLevelException, SetFuelLevelException


def test_burn_fuel_valid_params() -> None:
    """
    Проверка сжигания топлива у объекта.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}

    mock_burning_fuel_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_burning_fuel_obj}
    command_container.resolve("command.burn_fuel", params=params).execute()

    assert mock_burning_fuel_obj.get_fuel_level() == 90


def test_burn_fuel_impossible_read_fuel_level() -> None:
    """
    Проверка сжигания топлива у объекта, у которого невозможно прочитать текущий уровень топлива.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}

    class BurnFuelImplementation:
        def get_fuel_level(self) -> int:
            raise ReadFuelLevelException

        def set_fuel_level(self, volume: int) -> None:
            mock_obj["fuel_level"] = volume

        def get_required_fuel_level(self) -> int:
            return mock_obj["required_fuel_level"]

    params = {"obj": BurnFuelImplementation()}

    with pytest.raises(ReadFuelLevelException):
        command_container.resolve("command.burn_fuel", params=params).execute()


def test_burn_fuel_impossible_set_fuel_level() -> None:
    """
    Проверка сжигания топлива у объекта, у которого невозможно установить новый уровень топлива.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}

    class BurnFuelImplementation:
        def get_fuel_level(self) -> int:
            return mock_obj["fuel_level"]

        def set_fuel_level(self, volume: int) -> None:
            raise SetFuelLevelException

        def get_required_fuel_level(self) -> int:
            return mock_obj["required_fuel_level"]

    params = {"obj": BurnFuelImplementation()}

    with pytest.raises(SetFuelLevelException):
        command_container.resolve("command.burn_fuel", params=params).execute()


def test_burn_fuel_impossible_read_required_fuel_level() -> None:
    """
    Проверка сжигания топлива у объекта, у которого невозможно прочитать необходимый уровень топлива.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}

    class BurnFuelImplementation:
        def get_fuel_level(self) -> int:
            return mock_obj["fuel_level"]

        def set_fuel_level(self, volume: int) -> None:
            mock_obj["fuel_level"] = volume

        def get_required_fuel_level(self) -> int:
            raise ReadRequiredFuelLevelException

    params = {"obj": BurnFuelImplementation()}
    with pytest.raises(ReadRequiredFuelLevelException):
        command_container.resolve("command.burn_fuel", params=params).execute()
