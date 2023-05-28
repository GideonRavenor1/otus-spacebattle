from sqlite3 import Cursor

from src.game.factories.base import BaseObjectFactory
from src.game.repositories import AuthRepository


class AuthRepositoryFactory(BaseObjectFactory):
    def __call__(self, *, params: dict) -> AuthRepository:
        cursor: Cursor = params.get("cursor")
        if cursor is None:
            raise ValueError("Не указан объект Cursor")

        return self.object(cursor=cursor)

    @property
    def object(self) -> type[AuthRepository]:  # noqa A003
        return AuthRepository
