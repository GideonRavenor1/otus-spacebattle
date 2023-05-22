from typing import Optional, TYPE_CHECKING

from src.game.commands.base import BaseCommand
from src.game.exceptions import RegisterObjectException

if TYPE_CHECKING:
    from src.game.dependencies import IoCContainer


class RegisterObject(BaseCommand):
    def __init__(
        self,
        *,
        ioc_container: "IoCContainer",
        obj_name: str,
        obj: object,
        obj_map_name: Optional[str],
        **kwargs,
    ) -> None:
        self._ioc_container = ioc_container
        self._object_name = obj_name
        self._obj_map_name = obj_map_name
        self._obj = obj

    def execute(self) -> None:
        if self._object_name in self._ioc_container:
            msg = f"Объект {self._object_name} уже существует"
            raise RegisterObjectException(msg)
        self._ioc_container[self._object_name] = self._obj

        if self._obj_map_name is None:
            return

        self._ioc_container.objects_map[self._obj_map_name] = self._object_name
