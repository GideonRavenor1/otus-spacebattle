from src.game.factories.base import BaseObjectFactory
from src.game.repositories import AuthRepository
from src.game.workers import RabbitMQGameWorker


class RabbitMQGameWorkerFactory(BaseObjectFactory):
    def __call__(self, *, params: dict) -> RabbitMQGameWorker:
        repository: AuthRepository = params.get("repository")
        if repository is None:
            raise ValueError("Не указан объект AuthRepository")

        return self.object(repository=repository)

    @property
    def object(self) -> type[RabbitMQGameWorker]:  # noqa A003
        return RabbitMQGameWorker
