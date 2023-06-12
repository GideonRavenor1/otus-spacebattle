class OutOfMapRangeException(Exception):
    """Выход за границы карты"""


class PositionOccupiedException(Exception):
    """Позиция занята"""


class ObjectsCollided(Exception):
    """Столкновение объектов"""
