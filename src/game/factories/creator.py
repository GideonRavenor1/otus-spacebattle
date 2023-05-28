from src.game.factories.base import BaseObjectFactory
from src.game.game_object import GameObject
from src.game.vectors import Vector


class GameObjectFactory(BaseObjectFactory):
    def __call__(self, *, params: dict) -> GameObject:
        if "position" in params:
            params["position"] = Vector(*params["position"])
        if "velocity" in params:
            params["velocity"] = Vector(*params["velocity"])

        return self.object(data=params)

    @property
    def object(self) -> type[GameObject]:  # noqa A003
        return GameObject
