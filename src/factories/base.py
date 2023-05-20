from abc import ABC, abstractmethod

from src.commands import BaseCommand
from src.game_object import GameObject


class BaseObjectFactory(ABC):
    @abstractmethod
    def __call__(self, *, params: dict) -> GameObject:
        raise NotImplementedError

    @property
    @abstractmethod
    def object(self) -> type[GameObject]:  # noqa
        raise NotImplementedError


class BaseCommandFactory(ABC):
    @abstractmethod
    def __call__(self, *, params: dict) -> BaseCommand:
        raise NotImplementedError

    @property
    @abstractmethod
    def command(self) -> type[BaseCommand]:
        raise NotImplementedError
