from src.exceptions import (
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
from src.vectors import Vector


class GameObject:
    def __init__(self, data: dict) -> None:
        self._data = data

    def get_position(self) -> Vector:
        try:
            return self._data["position"]
        except KeyError:
            raise ReadPositionException

    def set_position(self, vector: Vector) -> None:
        try:
            self._data["position"] = vector
        except KeyError:
            raise SetPositionException

    def get_velocity(self) -> Vector:
        try:
            return self._data["velocity"]
        except KeyError:
            raise ReadVelocityException

    def get_fuel_level(self) -> int:
        try:
            return self._data["fuel_level"]
        except KeyError:
            raise ReadFuelLevelException

    def set_fuel_level(self, volume: int) -> None:
        try:
            self._data["fuel_level"] = volume
        except KeyError:
            raise SetFuelLevelException

    def get_required_fuel_level(self) -> int:
        try:
            return self._data["required_fuel_level"]
        except KeyError:
            raise ReadRequiredFuelLevelException

    def get_direction(self) -> int:
        try:
            return self._data["direction"]
        except KeyError:
            raise ReadDirectionException

    def get_angular_velocity(self) -> int:
        try:
            return self._data["angular_velocity"]
        except KeyError:
            raise ReadAngularVelocityException

    def get_direction_number(self) -> int:
        try:
            return self._data["direction_number"]
        except KeyError:
            raise RaedDirectionNumberException

    def set_direction(self, value: int) -> None:
        try:
            self._data["direction"] = value
        except KeyError:
            raise SetDirectionException

    def set_velocity(self, vector: Vector) -> None:
        try:
            self._data["velocity"] = vector
        except KeyError:
            raise SetVelocityException


def get_game_object(data: dict) -> "GameObject":
    return GameObject(data=data)
