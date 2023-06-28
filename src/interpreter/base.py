from abc import ABC, abstractmethod


class BaseInterpreter(ABC):
    @abstractmethod
    def interpret(self) -> None:
        raise NotImplementedError
