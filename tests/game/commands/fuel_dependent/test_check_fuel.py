import random

import pytest

from src.game.dependencies.game_objects_container import game_container
from src.game.dependencies.command_container import command_container
from src.game.exceptions import NoFuelException


def test_check_fuel_valid_params() -> None:
    """
    Проверка необходимого уровня топлива у объекта.
    """
    user_id = random.randint(1, 100)
    mock_obj = {"fuel_level": 100, "required_fuel_level": 10, "user_id": user_id}
    params = {"obj": game_container.resolve("game.objects.create.object", params=mock_obj)}

    try:
        command_container.resolve("command.check_fuel", params=params).execute()
    except NoFuelException:
        pytest.fail("Unexpected NoFuelError...")


def test_check_fuel_if_not_enough_fuel() -> None:
    """
    Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
    """
    user_id = random.randint(1, 100)
    mock_obj = {"fuel_level": 9, "required_fuel_level": 10, "user_id": user_id}
    params = {"obj": game_container.resolve("game.objects.create.object", params=mock_obj)}

    with pytest.raises(NoFuelException):
        command_container.resolve("command.check_fuel", params=params).execute()
