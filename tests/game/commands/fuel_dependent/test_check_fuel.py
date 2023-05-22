import pytest

from src.game.dependencies import container
from src.game.exceptions import NoFuelException


def test_check_fuel_valid_params() -> None:
    """
    Проверка необходимого уровня топлива у объекта.
    """

    mock_obj = {"fuel_level": 100, "required_fuel_level": 10}
    params = {"obj": container.resolve("game.objects.create", params=mock_obj)}

    try:
        container.resolve("command.check_fuel", params=params).execute()
    except NoFuelException:
        pytest.fail("Unexpected NoFuelError...")


def test_check_fuel_if_not_enough_fuel() -> None:
    """
    Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
    """

    mock_obj = {"fuel_level": 9, "required_fuel_level": 10}
    params = {"obj": container.resolve("game.objects.create", params=mock_obj)}

    with pytest.raises(NoFuelException):
        container.resolve("command.check_fuel", params=params).execute()