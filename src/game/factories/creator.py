import uuid

from src.game.factories.base import BaseObjectFactory
from src.game.game_object import GameMap, GameObject
from src.game.vectors import Vector


class GameObjectFactory(BaseObjectFactory):
    def __call__(self, *, params: dict) -> GameObject:
        object_id = str(uuid.uuid4())
        user_id = params.get("user_id")

        if user_id is None:
            raise ValueError("Не указан id пользователя")

        if "position" in params:
            params["position"] = Vector(*params["position"], object_id=object_id)
        if "velocity" in params:
            params["velocity"] = Vector(*params["velocity"], object_id=object_id)

        return self.object(data=params, object_id=object_id, user_id=user_id)

    @property
    def object(self) -> type[GameObject]:  # noqa A003
        return GameObject


class GameMapFactory(GameObjectFactory):
    @property
    def object(self) -> type[GameMap]:  # noqa A003
        return GameMap

    def __call__(self, *, params: dict) -> GameMap:
        map_size: list[int] | None = params["map_size"]
        if map_size is None:
            raise ValueError("Не указан размер карты")

        return self.object(height=map_size[0], width=map_size[1])
