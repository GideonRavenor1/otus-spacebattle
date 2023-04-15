from typing import TYPE_CHECKING

from src.commands import BaseCommand
from src.exceptions import RegisterCommandException

if TYPE_CHECKING:
    from src.dependencies import IoCContainer


class RegisterCommand(BaseCommand):
    def __init__(self, *, ioc_container: "IoCContainer", obj_name: str, obj: object, **kwargs) -> None:
        self._ioc_container = ioc_container
        self._object_name = obj_name
        self._obj = obj

    def execute(self) -> None:
        if self._object_name in self._ioc_container:
            msg = f"Объект {self._object_name} уже существует"
            raise RegisterCommandException(msg)
        self._ioc_container[self._object_name] = self._obj
