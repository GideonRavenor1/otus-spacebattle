from typing import Protocol


class NeedsFuel(Protocol):
	
	def get_fuel_level(self) -> int:
		...
	
	def set_fuel_level(self, volume: int) -> None:
		...
	
	def get_required_fuel_level(self) -> int:
		...
