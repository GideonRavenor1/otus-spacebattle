from abc import ABC, abstractmethod
from sqlite3 import Cursor


class BaseRepository(ABC):
    def __init__(self, cursor: Cursor) -> None:
        self._cursor = cursor

    @abstractmethod
    def select_one(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def insert(self, *args, **kwargs) -> None:
        raise NotImplementedError
