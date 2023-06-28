from typing import TYPE_CHECKING

from src.game.commands.base import BaseCommand
from src.game.exceptions import ObjectsCollided
from src.game.interfaces import Movable


if TYPE_CHECKING:
    from src.game.dependencies.base import IoCContainer


class CheckMapCollisionCommand(BaseCommand):
    def __init__(self, *, obj: Movable, game_id: str, ioc_container: "IoCContainer", **kwargs) -> None:
        self._obj = obj
        self._game_id = game_id
        self._ioc_container = ioc_container
        self._game_map = self._ioc_container.resolve(f"game.namespaces.{self._game_id}.map")

    def execute(self) -> None:
        vector = self._obj.get_position()
        try:
            self._game_map.move_vector(vector)
        except ObjectsCollided:
            another_vector = self._game_map.get_vector_at(vector.x, vector.y)
            self._game_map.remove_vector(vector)
            self._game_map.remove_vector(another_vector)

            self._obj.kill()
            another_object = self._ioc_container.resolve(
                f"game.namespaces.{self._game_id}.object_{another_vector.object_id}",
            )
            another_object.kill()
