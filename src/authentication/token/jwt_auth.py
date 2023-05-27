import jwt

from src.config import get_settings

setting = get_settings()


class JWTAuthentication:
    def __init__(self):
        self.secret = setting.AUTH_SECRET
        self.algorithm = setting.AUTH_ALGORITHM

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
