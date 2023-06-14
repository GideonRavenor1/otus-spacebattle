import uuid
from copy import deepcopy

from src.game.exceptions import (
    OutOfMapRangeException,
    PositionOccupiedException,
    RaedDirectionNumberException,
    ObjectsCollided,
    ReadAngularVelocityException,
    ReadDirectionException,
    ReadFuelLevelException,
    ReadPositionException,
    ReadRequiredFuelLevelException,
    ReadVelocityException,
    SetFuelLevelException,
)
from src.game.vectors import Vector

ZERO_FUEL_LEVEL = 0
ORIGIN_OF_COORDINATES = 0
INDEX_SHIFT = 1
CENTERING_COEFFICIENT = 2


class GameObject:
    def __init__(self, data: dict[str, Vector | int | list], object_id: str | None = None) -> None:
        self._id = str(uuid.uuid4()) if object_id is None else object_id
        self._data = data
        self._position: Vector | None = data.get("position")
        self._velocity: Vector | None = data.get("velocity")
        self._fuel_level: int | None = data.get("fuel_level")
        self._required_fuel_level: int | None = data.get("required_fuel_level")
        self._direction: int | None = data.get("direction")
        self._angular_velocity: int | None = data.get("angular_velocity")
        self._direction_number: int | None = data.get("direction_number")
        self._is_alive: bool = True

    def is_alive(self) -> bool:
        return self._is_alive

    def kill(self) -> None:
        self._is_alive = False

    def get_id(self) -> str:
        return self._id

    def get_position(self) -> Vector:
        if self._position is None:
            raise ReadPositionException("Не удалось прочитать положение объекта")
        return self._position

    def set_position(self, vector: Vector) -> None:
        self._position = vector

    def get_velocity(self) -> Vector:
        if self._velocity is None:
            raise ReadVelocityException("Не удалось прочитать скорость объекта")
        return self._velocity

    def get_fuel_level(self) -> int:
        if self._fuel_level is None:
            raise ReadFuelLevelException("Не удалось прочитать запас топлива объекта")
        return self._fuel_level

    def set_fuel_level(self, volume: int) -> None:
        if volume < ZERO_FUEL_LEVEL:
            raise SetFuelLevelException("Не удалось установить запас топлива объекта")
        self._fuel_level = volume

    def get_required_fuel_level(self) -> int:
        if self._required_fuel_level is None:
            raise ReadRequiredFuelLevelException("Не удалось прочитать необходимое количество топлива для действия")
        return self._required_fuel_level

    def get_direction(self) -> int:
        if self._direction is None:
            raise ReadDirectionException("Не удалось прочитать направление движения объекта")
        return self._direction

    def get_angular_velocity(self) -> int:
        if self._angular_velocity is None:
            raise ReadAngularVelocityException("Не удалось прочитать скорость поворота объекта")
        return self._angular_velocity

    def get_direction_number(self) -> int:
        if self._direction_number is None:
            raise RaedDirectionNumberException("Не удалось прочитать номер направления движения объекта")
        return self._direction_number

    def set_direction(self, value: int) -> None:
        self._direction = value

    def set_velocity(self, vector: Vector) -> None:
        self._velocity = vector

    @property
    def data(self) -> dict[str, Vector | int | list]:
        data = deepcopy(self._data)
        if "position" in data:
            data["position"]: Vector = data["position"].to_list()
        if "velocity" in data:
            data["velocity"]: Vector = data["velocity"].to_list()
        return data


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self._width: int = width
        self._height: int = height
        self._grid: list[list[Vector | None]] = [[None for _ in range(width)] for _ in range(height)]
        self._vector_positions = {}

    def set_vector_position(self, vector: Vector) -> None:
        x, y = self._get_grid_coords(vector)
        if self._if_position_occupied(x, y):
            raise PositionOccupiedException("Позиция уже занята")
        self._grid[y][x] = vector
        self._vector_positions[vector.object_id] = (x, y)

    def move_vector(self, vector: Vector) -> None:
        x, y = self._vector_positions[vector.object_id]
        x_new = vector.x - INDEX_SHIFT
        y_new = vector.y - INDEX_SHIFT

        if self._if_position_occupied(x_new, y_new):
            raise ObjectsCollided("Объекты столкнулись!")

        self._grid[x][y] = None

        self._grid[x_new][y_new] = vector
        self._vector_positions[vector.object_id] = (x_new, y_new)

    def remove_vector(self, vector: Vector) -> None:
        x, y = self._vector_positions[vector.object_id]
        self._grid[x - INDEX_SHIFT][y - INDEX_SHIFT] = None
        del self._vector_positions[vector.object_id]

    def get_vector_at(self, x: int, y: int) -> Vector | None:
        try:
            vector = self._grid[x - INDEX_SHIFT][y - INDEX_SHIFT]
        except IndexError:
            raise OutOfMapRangeException("Выход за пределы карты")
        return vector

    def _if_position_occupied(self, x: int, y: int) -> bool:
        return self._grid[y][x] is not None

    def _get_grid_coords(self, vector: Vector) -> tuple[int, int]:
        x = int(vector.x + self._width / CENTERING_COEFFICIENT)
        y = int(-vector.y + self._height / CENTERING_COEFFICIENT)
        if x < ORIGIN_OF_COORDINATES or x > self._width or y < ORIGIN_OF_COORDINATES or y > self._height:
            raise OutOfMapRangeException("Выход за пределы карты")
        return x - INDEX_SHIFT, y - INDEX_SHIFT
