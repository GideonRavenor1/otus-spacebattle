class NoFuelException(Exception):
    """Недостаточно топлива"""


class ReadFuelLevelException(Exception):
    """Ошибка при попытке получить текущий уровень топливо"""


class SetFuelLevelException(Exception):
    """Ошибка при попытке установить новый уровень топливо"""


class ReadRequiredFuelLevelException(Exception):
    """Ошибка при попытке получить необходимый уровень топлива"""
