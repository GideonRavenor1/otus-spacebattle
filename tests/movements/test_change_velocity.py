import pytest

from src.commands import ChangeVelocityCommand
from src.exceptions import ReadVelocityError, SetVelocityError
from src.vectors import Vector
from tests.utils import get_spaceship


def test_change_velocity_valid_params() -> None:
	"""
	Проверка модификации вектора мгновенной скорости при повороте.
	"""
	
	mock_obj = {
		"velocity": Vector(-7, 3),
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	obj = get_spaceship(data=mock_obj)
	ChangeVelocityCommand(obj).execute()
	
	assert obj.get_velocity() == Vector(90, 210)
	

def test_change_velocity_impossible_set_velocity() -> None:
	"""
	Проверка модификации вектора мгновенной скорости при повороте, если невозможно изменить мгновенную скорость.
	"""
	
	mock_obj = {
		"velocity": Vector(-7, 3),
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class ChangeVelocityImplementation:
		
		def get_velocity(self) -> Vector:
			return mock_obj["velocity"]
		
		def set_velocity(self, vector: Vector) -> None:
			raise SetVelocityError
	
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
		
	
	with pytest.raises(SetVelocityError):
		ChangeVelocityCommand(ChangeVelocityImplementation()).execute()


def test_change_velocity_impossible_read_velocity() -> None:
	"""
	Проверка модификации вектора мгновенной скорости при повороте, если объект невозможен прочитать мгновенную скорость.
	"""
	
	mock_obj = {
		"velocity": Vector(-7, 3),
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class ChangeVelocityImplementation:
		
		def get_velocity(self) -> Vector:
			raise ReadVelocityError
		
		def set_velocity(self, vector: Vector) -> None:
			mock_obj["velocity"] = vector
		
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
	
	
	with pytest.raises(ReadVelocityError):
		ChangeVelocityCommand(ChangeVelocityImplementation()).execute()


def test_change_velocity_impossible_read_angular_velocity() -> None:
	"""
	Проверка модификации вектора мгновенной скорости при повороте, если невозможно прочитать угловую скорость
	"""
	
	mock_obj = {
		"velocity": Vector(-7, 3),
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class ChangeVelocityImplementation:
		
		def get_velocity(self) -> Vector:
			raise ReadVelocityError
		
		def set_velocity(self, vector: Vector) -> None:
			mock_obj["velocity"] = vector
		
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
	
	
	with pytest.raises(ReadVelocityError):
		ChangeVelocityCommand(ChangeVelocityImplementation()).execute()
