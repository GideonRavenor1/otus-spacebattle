from abc import ABC, abstractmethod

from src.commands import BaseCommand


class BaseCommandFactory(ABC):
    @abstractmethod
    def create(self, *, params: dict) -> BaseCommand:
        raise NotImplementedError

    @property
    @abstractmethod
    def command(self) -> type[BaseCommand]:
        raise NotImplementedError
