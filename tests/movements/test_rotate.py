import pytest

from src.commands import Rotate
from src.exceptions import (
	ReadDirectionError,
	ReadAngularVelocityError,
	RaedDirectionNumberError,
	SetDirectionError,
)


@pytest.mark.parametrize(
	"direction, angular_velocity, direction_number, expected",
	[(270, 30, 360, 300), (200, 0, 360, 200)]
)
def test_rotate_valid_param(direction: int, angular_velocity: int, direction_number: int, expected: int) -> None:
	"""
	Положительные тесты, включающую нулевую угловую скорость
	"""
	
	mock_obj = {
		"direction": direction,
		"angular_velocity": angular_velocity,
		"direction_number": direction_number
	}
	
	class RotatableImplementation:
		
		def get_direction(self) -> int:
			return mock_obj["direction"]
	
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
		
		def get_direction_number(self) -> int:
			return mock_obj["direction_number"]
		
		def set_direction(self, value: int) -> None:
			mock_obj["direction"] = value
		
	mock_rotate = RotatableImplementation()
	Rotate(obj=mock_rotate).execute()
	
	assert mock_rotate.get_direction() == expected


def test_rotate_impossible_read_direction() -> None:
	"""
	Попытка повернуть объект, у которого невозможно прочитать текущее направление в пространстве, приводит к ошибке
	"""
	
	mock_obj = {
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class RotatableImplementation:
		
		def get_direction(self) -> int:
			raise ReadDirectionError
		
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
		
		def get_direction_number(self) -> int:
			return mock_obj["direction_number"]
		
		def set_direction(self, value: int) -> None:
			mock_obj["direction"] = value
	
	
	mock_rotate = RotatableImplementation()
	with pytest.raises(ReadDirectionError):
		Rotate(obj=mock_rotate).execute()


def test_rotate_impossible_read_angular_velocity() -> None:
	"""
	Попытка повернуть объект, у которого невозможно прочитать угловую скорость, приводит к ошибке
	"""
	
	mock_obj = {
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class RotatableImplementation:
		
		def get_direction(self) -> int:
			return mock_obj["direction"]
		
		def get_angular_velocity(self) -> int:
			raise ReadAngularVelocityError
		
		def get_direction_number(self) -> int:
			return mock_obj["direction_number"]
		
		def set_direction(self, value: int) -> None:
			mock_obj["direction"] = value
	
	
	mock_rotate = RotatableImplementation()
	with pytest.raises(ReadAngularVelocityError):
		Rotate(obj=mock_rotate).execute()


def test_rotate_impossible_set_direction() -> None:
	"""
	Попытка повернуть объект, у которого невозможно изменить текущее направление в пространстве, приводит к ошибке
	"""
	
	mock_obj = {
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class RotatableImplementation:
		
		def get_direction(self) -> int:
			return mock_obj["direction"]
		
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
		
		def get_direction_number(self) -> int:
			return mock_obj["direction_number"]
		
		def set_direction(self, value: int) -> None:
			raise SetDirectionError
	
	
	mock_rotate = RotatableImplementation()
	with pytest.raises(SetDirectionError):
		Rotate(obj=mock_rotate).execute()


def test_rotate_impossible_read_direction_number() -> None:
	"""
	Попытка повернуть объект, у которого невозможно прочитать номер направления, приводит к ошибке
	"""
	
	mock_obj = {
		"direction": 100,
		"angular_velocity": 30,
		"direction_number": 360
	}
	
	
	class RotatableImplementation:
		
		def get_direction(self) -> int:
			return mock_obj["direction"]
		
		def get_angular_velocity(self) -> int:
			return mock_obj["angular_velocity"]
		
		def get_direction_number(self) -> int:
			raise RaedDirectionNumberError
		
		def set_direction(self, value: int) -> None:
			mock_obj["direction_number"] = value
	
	
	mock_rotate = RotatableImplementation()
	with pytest.raises(RaedDirectionNumberError):
		Rotate(obj=mock_rotate).execute()