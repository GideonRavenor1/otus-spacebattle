from src.game.dependencies.base import IoCContainer
from src.game.factories import GameObjectFactory, GameMapFactory

game_container = IoCContainer()


game_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "game.objects.create.object",
        "obj": GameObjectFactory(),
        "object_map_name": None,
    },
)
game_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "game.objects.create.map",
        "obj": GameMapFactory(),
        "object_map_name": None,
    },
)
