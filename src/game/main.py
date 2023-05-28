import sqlite3
from pathlib import Path
from sqlite3 import Cursor, Connection

from src.game.dependencies.services_container import services_container
from src.game.repositories import AuthRepository
from src.game.repositories.utils import create_table
from src.game.workers import RabbitMQGameWorker
from src.game.workers.base import BaseWorker
from src.config import get_settings

settings = get_settings()


def main(worker: BaseWorker, connection: Connection, cursor: Cursor) -> None:
    try:
        create_table(cursor)
        worker.start_consuming()
    finally:
        worker.close()
        cursor.close()
        connection.close()
        Path(settings.AUTH_DB).unlink()


if __name__ == "__main__":
    connection_ = sqlite3.connect(settings.AUTH_DB)
    cursor_ = connection_.cursor()

    repository: AuthRepository = services_container.resolve("services.repository.create", params={"cursor": cursor_})
    worker_: RabbitMQGameWorker = services_container.resolve(
        "services.workers.create",
        params={"repository": repository},
    )
    main(worker_, connection_, cursor_)
