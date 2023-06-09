import random

import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import CommandException
from src.game.vectors import Vector


def test_forward_movement_valid_params() -> None:
    """
    Проверка работы макрокоманды. Валидные параметры.
    """
    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [-7, 3],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "user_id": user_id,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}
    macro_command = command_container.resolve("command.forward", params=params)
    macro_command.execute()

    assert mock_space_ship_obj.get_position() == Vector(5, 8, mock_space_ship_obj.get_id())
    assert mock_space_ship_obj.get_fuel_level() == 90


def test_forward_movement_if_not_enough_fuel() -> None:
    """
    Проверка работы макрокоманды. Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
    """
    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [-7, 3],
        "fuel_level": 9,
        "required_fuel_level": 10,
        "user_id": user_id,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}
    macro_command = command_container.resolve("command.forward", params=params)
    with pytest.raises(CommandException):
        macro_command.execute()


def test_forward_movement_if_object_remains_in_place() -> None:
    """
    Проверка работы макрокоманды. После сдвига объекта он остается на месте.
    """
    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [0, 0],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "user_id": user_id,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}
    macro_command = command_container.resolve("command.forward", params=params)
    with pytest.raises(CommandException):
        macro_command.execute()
