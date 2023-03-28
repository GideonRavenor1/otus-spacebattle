from src.commands.base import BaseCommand
from src.interfaces import Movable


class Move(BaseCommand):
	def __init__(self, obj: Movable) -> None:
		self._obj = obj
		
	def execute(self) -> None:
		self._obj.set_position(self._obj.get_position() + self._obj.get_velocity())
