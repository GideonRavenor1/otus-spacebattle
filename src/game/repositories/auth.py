from src.game.exceptions import AuthenticationException
from src.game.repositories.base import BaseRepository
from src.config import get_settings

settings = get_settings()


class AuthRepository(BaseRepository):
    AUTH_TABLE = settings.AUTH_TABLE

    def select_one(self, token: str, user_id: int) -> str:
        jwt_token = self._cursor.execute(
            f"SELECT jwt FROM {self.AUTH_TABLE} WHERE user_id = {user_id} AND jwt = '{token}'",
        ).fetchone()
        if jwt_token is None:
            raise AuthenticationException("Не верный токен")
        return jwt_token[0]

    def insert(self, token: str, user_id: int) -> None:
        self._cursor.execute(f"INSERT INTO {self.AUTH_TABLE} (user_id, jwt) VALUES ({user_id}, '{token}')")
