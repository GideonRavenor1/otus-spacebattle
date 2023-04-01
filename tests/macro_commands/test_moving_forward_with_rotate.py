import pytest

from src.commands import (
	BaseMacroCommand, BurnFuelCommand, ChangeVelocityCommand, CheckFuelCommand, MoveCommand, RotateCommand,
)
from src.exceptions import CommandException
from src.vectors import Vector
from tests.utils import get_spaceship


def test_moving_forward_with_rotate_valid_params() -> None:
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3),
		"fuel_level": 100,
		"required_fuel_level": 10,
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	mock_space_ship_obj = get_spaceship(data=mock_obj)
	commands = [
		CheckFuelCommand(obj=mock_space_ship_obj),
		MoveCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
		
		CheckFuelCommand(obj=mock_space_ship_obj),
		RotateCommand(obj=mock_space_ship_obj),
		ChangeVelocityCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
	]
	BaseMacroCommand(commands).execute()
	
	assert mock_space_ship_obj.get_position() == Vector(5, 8)
	assert mock_space_ship_obj.get_fuel_level() == 80


def test_forward_movement_if_not_enough_fuel() -> None:
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3),
		"fuel_level": 19,
		"required_fuel_level": 10,
	}
	
	mock_space_ship_obj = get_spaceship(data=mock_obj)
	commands = [
		CheckFuelCommand(obj=mock_space_ship_obj),
		MoveCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
		
		CheckFuelCommand(obj=mock_space_ship_obj),
		RotateCommand(obj=mock_space_ship_obj),
		ChangeVelocityCommand(obj=mock_space_ship_obj),
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
		
		CheckFuelCommand(obj=mock_space_ship_obj),
		RotateCommand(obj=mock_space_ship_obj),
		ChangeVelocityCommand(obj=mock_space_ship_obj),
		BurnFuelCommand(obj=mock_space_ship_obj),
	]
	with pytest.raises(CommandException):
		BaseMacroCommand(commands).execute()
