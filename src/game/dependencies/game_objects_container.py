from src.game.dependencies.base import IoCContainer
from src.game.factories import GameObjectFactory

game_container = IoCContainer()


game_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "game.objects.create",
        "obj": GameObjectFactory(),
        "object_map_name": None,
    },
)
