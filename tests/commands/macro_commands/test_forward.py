import pytest

from src.exceptions import CommandException
from src.factories import ForwardMacroCommandFactory
from src.vectors import Vector
from tests.utils import get_game_object


def test_forward_movement_valid_params() -> None:
    """
    Проверка работы макрокоманды. Валидные параметры.
    """

    mock_obj = {
        "position": Vector(12, 5),
        "velocity": Vector(-7, 3),
        "fuel_level": 100,
        "required_fuel_level": 10,
    }

    mock_space_ship_obj = get_game_object(data=mock_obj)
    macro_command = ForwardMacroCommandFactory(obj=mock_space_ship_obj).create()
    macro_command.execute()

    assert mock_space_ship_obj.get_position() == Vector(5, 8)
    assert mock_space_ship_obj.get_fuel_level() == 90


def test_forward_movement_if_not_enough_fuel() -> None:
    """
    Проверка работы макрокоманды. Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
    """

    mock_obj = {
        "position": Vector(12, 5),
        "velocity": Vector(-7, 3),
        "fuel_level": 9,
        "required_fuel_level": 10,
    }

    mock_space_ship_obj = get_game_object(data=mock_obj)
    macro_command = ForwardMacroCommandFactory(obj=mock_space_ship_obj).create()
    with pytest.raises(CommandException):
        macro_command.execute()


def test_forward_movement_if_object_remains_in_place() -> None:
    """
    Проверка работы макрокоманды. После сдвига объекта он остается на месте.
    """

    mock_obj = {
        "position": Vector(12, 5),
        "velocity": Vector(0, 0),
        "fuel_level": 100,
        "required_fuel_level": 10,
    }

    mock_space_ship_obj = get_game_object(data=mock_obj)
    mock_space_ship_obj = get_game_object(data=mock_obj)
    macro_command = ForwardMacroCommandFactory(obj=mock_space_ship_obj).create()
    with pytest.raises(CommandException):
        macro_command.execute()
