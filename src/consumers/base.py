from abc import ABC, abstractmethod


class BaseConsumer(ABC):
    @abstractmethod
    def start_consuming(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
