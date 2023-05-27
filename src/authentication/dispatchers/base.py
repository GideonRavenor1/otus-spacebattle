from typing import Any

from src.authentication.token.jwt_auth import JWTAuthentication


class Dispatcher:
    _authentication = JWTAuthentication()

    def dispatch(self, action: str, params: dict) -> dict:
        method = getattr(self, f"_handle_{action}", None)
        if method is None:
            msg = f"Ошибка диспетчеризации, метод {action} не реализован"
            raise ValueError(msg)

        return method(params=params)

    def _handle_get_token(self, params: dict) -> dict:
        user_id = params.get("user_id")
        payload = {"user_id": user_id}
        token = self._authentication.encode(payload=payload)
        return {"token": token, "user_id": user_id, "action": "save_token"}

    @staticmethod
    def _check_object(object_: Any, name: str) -> None:
        if object_ is None:
            msg = f"{name} обязательное поле"
            raise ValueError(msg)
