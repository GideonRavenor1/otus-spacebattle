import pytest

from src.dependencies import container
from src.exceptions import NoFuelException
from tests.utils import get_game_object


def test_check_fuel_valid_params() -> None:
    """
    Проверка необходимого уровня топлива у объекта.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}
    params = {"obj": get_game_object(data=mock_obj)}

    try:
        container.resolve("check_fuel", params=params).execute()
    except NoFuelException:
        pytest.fail("Unexpected NoFuelError...")


def test_check_fuel_if_not_enough_fuel() -> None:
    """
    Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
    """

    mock_obj = {"fuel_level": 9, "required_fuel_level": 10}
    params = {"obj": get_game_object(data=mock_obj)}

    with pytest.raises(NoFuelException):
        container.resolve("check_fuel", params=params).execute()
