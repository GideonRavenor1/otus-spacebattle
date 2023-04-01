import pytest

from src.commands import BurnFuelCommand
from src.exceptions import ReadFuelLevelError, ReadRequiredFuelLevelError, SetFuelLevelError
from tests.utils import get_spaceship


def test_burn_fuel_valid_params() -> None:
	"""
	Проверка сжигания топлива у объекта.
	"""
	
	mock_obj = {
		"fuel_level": 100,
		"required_fuel_level": 10
	}
	
	mock_burning_fuel_obj = get_spaceship(data=mock_obj)
	BurnFuelCommand(obj=mock_burning_fuel_obj).execute()
	
	assert mock_burning_fuel_obj.get_fuel_level() == 90
	
	
def test_burn_fuel_impossible_read_fuel_level() -> None:
	"""
	Проверка сжигания топлива у объекта, у которого невозможно прочитать текущий уровень топлива.
	"""
	
	mock_obj = {
		"fuel_level": 100,
		"required_fuel_level": 10
	}
	
	
	class BurnFuelImplementation:
		
		def get_fuel_level(self) -> int:
			raise ReadFuelLevelError
		
		def set_fuel_level(self, volume: int) -> None:
			mock_obj["fuel_level"] = volume
		
		def get_required_fuel_level(self) -> int:
			return mock_obj["required_fuel_level"]
	
	with pytest.raises(ReadFuelLevelError):
		BurnFuelCommand(obj=BurnFuelImplementation()).execute()


def test_burn_fuel_impossible_set_fuel_level() -> None:
	"""
	Проверка сжигания топлива у объекта, у которого невозможно установить новый уровень топлива.
	"""
	
	mock_obj = {
		"fuel_level": 100,
		"required_fuel_level": 10
	}
	
	
	class BurnFuelImplementation:
		
		def get_fuel_level(self) -> int:
			return mock_obj["fuel_level"]
		
		def set_fuel_level(self, volume: int) -> None:
			raise SetFuelLevelError
		
		def get_required_fuel_level(self) -> int:
			return mock_obj["required_fuel_level"]
	
	
	with pytest.raises(SetFuelLevelError):
		BurnFuelCommand(obj=BurnFuelImplementation()).execute()


def test_burn_fuel_impossible_read_required_fuel_level() -> None:
	"""
	Проверка сжигания топлива у объекта, у которого невозможно прочитать необходимый уровень топлива.
	"""
	
	mock_obj = {
		"fuel_level": 100,
		"required_fuel_level": 10
	}
	
	
	class BurnFuelImplementation:
		
		def get_fuel_level(self) -> int:
			return mock_obj["fuel_level"]
		
		def set_fuel_level(self, volume: int) -> None:
			mock_obj["fuel_level"] = volume
		
		def get_required_fuel_level(self) -> int:
			raise ReadRequiredFuelLevelError
	
	
	with pytest.raises(ReadRequiredFuelLevelError):
		BurnFuelCommand(obj=BurnFuelImplementation()).execute()
