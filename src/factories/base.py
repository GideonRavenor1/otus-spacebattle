from abc import ABC, abstractmethod

from src.commands import BaseCommand


class BaseCommandFactory(ABC):
    @abstractmethod
    def __call__(self, *, params: dict) -> BaseCommand:
        raise NotImplementedError

    @property
    @abstractmethod
    def command(self) -> type[BaseCommand]:
        raise NotImplementedError
