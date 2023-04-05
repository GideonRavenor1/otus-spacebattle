import pytest

from src.factories import COMMAND_FACTORIES
from src.exceptions import ReadFuelLevelException, ReadRequiredFuelLevelException, SetFuelLevelException
from tests.utils import get_game_object


def test_burn_fuel_valid_params() -> None:
    """
    Проверка сжигания топлива у объекта.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}

    mock_burning_fuel_obj = get_game_object(data=mock_obj)
    params = {"obj": mock_burning_fuel_obj}
    COMMAND_FACTORIES["burn_fuel"].create(params=params).execute()

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
        COMMAND_FACTORIES["burn_fuel"].create(params=params).execute()


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
        COMMAND_FACTORIES["burn_fuel"].create(params=params).execute()


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
        COMMAND_FACTORIES["burn_fuel"].create(params=params).execute()
