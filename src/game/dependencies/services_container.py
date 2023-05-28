from src.game.dependencies.base import IoCContainer
from src.game.factories.repository import AuthRepositoryFactory
from src.game.factories.workers import RabbitMQGameWorkerFactory

services_container = IoCContainer()


services_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "services.repository.create",
        "obj": AuthRepositoryFactory(),
        "object_map_name": None,
    },
)
services_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "services.workers.create",
        "obj": RabbitMQGameWorkerFactory(),
        "object_map_name": None,
    },
)
