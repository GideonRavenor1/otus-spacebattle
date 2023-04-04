from abc import ABC, abstractmethod

from src.commands import BaseCommand


class BaseCommandFactory(ABC):
    def __init__(self, *, params: dict) -> None:
        self._params = params

    @abstractmethod
    def create(self) -> BaseCommand:
        raise NotImplementedError

    @property
    @abstractmethod
    def command(self) -> BaseCommand:
        raise NotImplementedError
