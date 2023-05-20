from collections import UserDict
from typing import Optional

from src.commands import BaseCommand, RegisterObject
from src.exceptions import ResolveDependencyException


class IoCContainer(UserDict):
    objects_map = {}

    def __init__(self) -> None:
        super().__init__()
        self.data["ioc.register"] = lambda params: RegisterObject(
            ioc_container=self,
            obj_name=params["obj_name"],
            obj=params["obj"],
            obj_map_name=params.get("object_map_name"),
        ).execute()

    def resolve(self, object_name: str, params: Optional[dict] = None) -> object | BaseCommand:
        if object_name in self.objects_map:
            return self[self.objects_map[object_name]](params=params)

        if object_name in self:
            return self[object_name](params=params)

        msg = f"Объект {object_name} не существует"
        raise ResolveDependencyException(msg)
