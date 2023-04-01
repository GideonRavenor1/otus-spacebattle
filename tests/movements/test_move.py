import pytest

from src.commands import MoveCommand
from src.exceptions import ReadPositionError, ReadVelocityError, SetPositionError
from src.vectors import Vector
from tests.utils import get_spaceship


def test_move_valid_params() -> None:
	"""
	Для объекта, находящегося в точке (12, 5) и движущегося со скоростью (-7, 3)
	движение меняет положение объекта на (5, 8)
	"""
	
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3)
	}
	
	mock_movable_obj = get_spaceship(data=mock_obj)
	MoveCommand(obj=mock_movable_obj).execute()
	
	assert mock_movable_obj.get_position() == Vector(5, 8)


def test_move_impossible_read_position() -> None:
	"""
	Попытка сдвинуть объект, у которого невозможно прочитать положение в пространстве, приводит к ошибке
	"""
	
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3)
	}
	
	
	class MovableImplementation:
		
		def get_position(self) -> Vector:
			raise ReadPositionError
		
		def set_position(self, vector: Vector) -> None:
			mock_obj["position"] = vector
		
		def get_velocity(self) -> Vector:
			return mock_obj["velocity"]
	
	
	mock_movable_obj = MovableImplementation()
	with pytest.raises(ReadPositionError):
		MoveCommand(obj=mock_movable_obj).execute()


def test_move_if_object_remains_in_place() -> None:
	"""
	После сдвига объекта он остаелся на месте.
	"""
	
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(0, 0)
	}
	
	mock_movable_obj = get_spaceship(data=mock_obj)
	with pytest.raises(SetPositionError):
		MoveCommand(obj=mock_movable_obj).execute()


def test_move_impossible_read_velocity() -> None:
	"""
	Попытка сдвинуть объект, у которого невозможно прочитать значение мгновенной скорости, приводит к ошибке
	"""
	
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3)
	}
	
	
	class MovableImplementation:
		
		def get_position(self) -> Vector:
			return mock_obj["position"]
		
		def set_position(self, vector: Vector) -> None:
			mock_obj["position"] = vector
		
		def get_velocity(self) -> Vector:
			raise ReadVelocityError
	
	
	mock_movable_obj = MovableImplementation()
	with pytest.raises(ReadVelocityError):
		MoveCommand(obj=mock_movable_obj).execute()


def test_move_impossible_set_position() -> None:
	"""
	Попытка сдвинуть объект, у которого невозможно изменить положение в пространстве, приводит к ошибке
	"""
	
	mock_obj = {
		"position": Vector(12, 5),
		"velocity": Vector(-7, 3)
	}
	
	
	class MovableImplementation:
		
		def get_position(self) -> Vector:
			return mock_obj["position"]
		
		def set_position(self, vector: Vector) -> None:
			raise SetPositionError
		
		def get_velocity(self) -> Vector:
			return mock_obj["velocity"]
	
	
	mock_movable_obj = MovableImplementation()
	with pytest.raises(SetPositionError):
		MoveCommand(obj=mock_movable_obj).execute()
