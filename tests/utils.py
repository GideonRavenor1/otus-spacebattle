from src.exceptions import (
	RaedDirectionNumberError, ReadAngularVelocityError, ReadDirectionError, ReadFuelLevelError, ReadPositionError,
	ReadRequiredFuelLevelError, ReadVelocityError, SetDirectionError, SetFuelLevelError, SetPositionError,
	SetVelocityError,
)
from src.vectors import Vector


class Spaceship:
	
	def __init__(self, data: dict) -> None:
		self._data = data
	
	def get_position(self) -> Vector:
		try:
			return self._data["position"]
		except KeyError:
			raise ReadPositionError
	
	def set_position(self, vector: Vector) -> None:
		try:
			self._data["position"] = vector
		except KeyError:
			raise SetPositionError
	
	def get_velocity(self) -> Vector:
		try:
			return self._data["velocity"]
		except KeyError:
			raise ReadVelocityError
	
	def get_fuel_level(self) -> int:
		try:
			return self._data["fuel_level"]
		except KeyError:
			raise ReadFuelLevelError

	def set_fuel_level(self, volume: int) -> None:
		try:
			self._data["fuel_level"] = volume
		except KeyError:
			raise SetFuelLevelError
	
	def get_required_fuel_level(self) -> int:
		try:
			return self._data["required_fuel_level"]
		except KeyError:
			raise ReadRequiredFuelLevelError
	
	def get_direction(self) -> int:
		try:
			return self._data["direction"]
		except KeyError:
			raise ReadDirectionError
	
	def get_angular_velocity(self) -> int:
		try:
			return self._data["angular_velocity"]
		except KeyError:
			raise ReadAngularVelocityError
	
	def get_direction_number(self) -> int:
		try:
			return self._data["direction_number"]
		except KeyError:
			raise RaedDirectionNumberError
	
	def set_direction(self, value: int) -> None:
		try:
			self._data["direction"] = value
		except KeyError:
			raise SetDirectionError
	
	def set_velocity(self, vector: Vector) -> None:
		try:
			self._data["velocity"] = vector
		except KeyError:
			raise SetVelocityError


def get_spaceship(data: dict) -> "Spaceship":
	"""

	:rtype: object
	"""
	return Spaceship(data=data)
