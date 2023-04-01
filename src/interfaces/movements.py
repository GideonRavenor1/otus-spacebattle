from typing import Protocol

from src.vectors import Vector


class Movable(Protocol):
	
	def get_position(self) -> Vector:
		...
	
	def set_position(self, vector: Vector) -> None:
		...
	
	def get_velocity(self) -> Vector:
		...


class Rotatable(Protocol):
	
	def get_direction(self) -> int:
		...
	
	def get_angular_velocity(self) -> int:
		...
	
	def get_direction_number(self) -> int:
		...

	def set_direction(self, direction: int) -> None:
		...


class VelocityChanger(Protocol):
	
	def get_velocity(self) -> Vector:
		...
	
	def get_angular_velocity(self) -> int:
		...
	
	def set_velocity(self, vector: Vector) -> None:
		...
	