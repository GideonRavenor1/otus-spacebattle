from src.game.exceptions import (
    RaedDirectionNumberException,
    ReadAngularVelocityException,
    ReadDirectionException,
    ReadFuelLevelException,
    ReadPositionException,
    ReadRequiredFuelLevelException,
    ReadVelocityException,
    SetDirectionException,
    SetFuelLevelException,
    SetPositionException,
    SetVelocityException,
)
from src.game.vectors import Vector


class GameObject:
    def __init__(self, data: dict) -> None:
        self._data = data

    def get_position(self) -> Vector:
        try:
            return self._data["position"]
        except KeyError:
            raise ReadPositionException("Не удалось прочитать положение объекта")

    def set_position(self, vector: Vector) -> None:
        try:
            self._data["position"] = vector
        except KeyError:
            raise SetPositionException("Не удалось установить положение объекта")

    def get_velocity(self) -> Vector:
        try:
            return self._data["velocity"]
        except KeyError:
            raise ReadVelocityException("Не удалось прочитать скорость объекта")

    def get_fuel_level(self) -> int:
        try:
            return self._data["fuel_level"]
        except KeyError:
            raise ReadFuelLevelException("Не удалось прочитать запас топлива объекта")

    def set_fuel_level(self, volume: int) -> None:
        try:
            self._data["fuel_level"] = volume
        except KeyError:
            raise SetFuelLevelException("Не удалось установить запас топлива объекта")

    def get_required_fuel_level(self) -> int:
        try:
            return self._data["required_fuel_level"]
        except KeyError:
            raise ReadRequiredFuelLevelException("Не удалось прочитать необходимое количество топлива для действия")

    def get_direction(self) -> int:
        try:
            return self._data["direction"]
        except KeyError:
            raise ReadDirectionException("Не удалось прочитать направление движения объекта")

    def get_angular_velocity(self) -> int:
        try:
            return self._data["angular_velocity"]
        except KeyError:
            raise ReadAngularVelocityException("Не удалось прочитать скорость поворота объекта")

    def get_direction_number(self) -> int:
        try:
            return self._data["direction_number"]
        except KeyError:
            raise RaedDirectionNumberException("Не удалось прочитать номер направления движения объекта")

    def set_direction(self, value: int) -> None:
        try:
            self._data["direction"] = value
        except KeyError:
            raise SetDirectionException("Не удалось установить направление движения объекта")

    def set_velocity(self, vector: Vector) -> None:
        try:
            self._data["velocity"] = vector
        except KeyError:
            raise SetVelocityException("Не удалось установить скорость движения объекта")
