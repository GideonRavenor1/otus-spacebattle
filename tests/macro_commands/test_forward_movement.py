import pytest

from src.commands import BaseMacroCommand, BurnFuelCommand, CheckFuelCommand, MoveCommand
from src.exceptions import CommandException
from src.vectors import Vector
from tests.utils import get_spaceship


def test_forward_movement_valid_params() -> None:
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3),
		"fuel_level": 100,
		"required_fuel_level": 10,
	}
	
	mock_space_ship_obj = get_spaceship(data=mock_obj)
	commands = [
		CheckFuelCommand(obj=mock_space_ship_obj),
		MoveCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
	]
	BaseMacroCommand(commands).execute()
	
	assert mock_space_ship_obj.get_position() == Vector(5, 8)
	assert mock_space_ship_obj.get_fuel_level() == 90


def test_forward_movement_if_not_enough_fuel() -> None:
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3),
		"fuel_level": 9,
		"required_fuel_level": 10,
	}
	
	mock_space_ship_obj = get_spaceship(data=mock_obj)
	commands = [
		CheckFuelCommand(obj=mock_space_ship_obj),
		MoveCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
	]
	with pytest.raises(CommandException):
		BaseMacroCommand(commands).execute()


def test_forward_movement_if_object_remains_in_place() -> None:
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(0, 0),
		"fuel_level": 100,
		"required_fuel_level": 10,
	}
	
	mock_space_ship_obj = get_spaceship(data=mock_obj)
	commands = [
		CheckFuelCommand(obj=mock_space_ship_obj),
		MoveCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
	]
	with pytest.raises(CommandException):
		BaseMacroCommand(commands).execute()
