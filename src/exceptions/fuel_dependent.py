class NoFuelError(Exception):
	"""Недостаточно топлива"""


class ReadFuelLevelError(Exception):
	"""Ошибка при попытке получить текущий уровень топливо"""
	
	
class SetFuelLevelError(Exception):
	"""Ошибка при попытке установить новый уровень топливо"""
	
	
class ReadRequiredFuelLevelError(Exception):
	"""Ошибка при попытке получить необходимый уровень топлива"""
