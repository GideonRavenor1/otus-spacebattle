from collections import UserDict

from src.commands.register import RegisterCommand
from src.exceptions import ResolveDependencyException


class IoCContainer(UserDict):
    def __init__(self) -> None:
        super().__init__()
        self.data["ioc.register"] = lambda params: RegisterCommand(
            ioc_container=self,
            obj_name=params["obj_name"],
            obj=params["obj"],
        ).execute()

    def resolve(self, object_name: str, params: dict) -> object:
        if object_name not in self:
            msg = f"Объект {object_name} не существует"
            raise ResolveDependencyException(msg)

        return self[object_name](params=params)
