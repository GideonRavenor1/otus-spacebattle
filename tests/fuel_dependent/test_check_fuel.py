import pytest

from src.commands.fuel_dependent import CheckFuelCommand
from src.exceptions import NoFuelError
from tests.utils import get_spaceship


def test_check_fuel_valid_params() -> None:
	"""
	Проверка необходимого уровня топлива у объекта.
	"""
	
	mock_obj = {
		"fuel_level": 100,
		"required_fuel_level": 10
	}
	
	try:
		CheckFuelCommand(obj=get_spaceship(data=mock_obj)).execute()
	except NoFuelError:
		pytest.fail("Unexpected NoFuelError...")


def test_check_fuel_if_not_enough_fuel() -> None:
	"""
	Проверка необходимого уровня топлива у объекта, если недостаточно топлива.
	"""
	
	mock_obj = {
		"fuel_level": 9,
		"required_fuel_level": 10
	}
	
	with pytest.raises(NoFuelError):
		CheckFuelCommand(obj=get_spaceship(data=mock_obj)).execute()
