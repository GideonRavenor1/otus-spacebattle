class ReadPositionException(Exception):
    """Ошибка при попытке получить позицию объекта"""


class ReadVelocityException(Exception):
    """Ошибка при попытке получить скорость объекта"""


class SetPositionException(Exception):
    """Ошибка при попытке установить позицию объекта"""


class SetVelocityException(Exception):
    """Ошибка при попытке установить скорость объекта"""
