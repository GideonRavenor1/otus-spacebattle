from abc import ABC, abstractmethod


class BaseWorker(ABC):
    @abstractmethod
    def start_consuming(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
