import sqlite3
from pathlib import Path
from sqlite3 import Cursor, Connection

from src.game.factories.repository import AuthRepositoryFactory
from src.game.factories.workers import RabbitMQGameWorkerFactory
from src.game.repositories.utils import create_table
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
    repository = AuthRepositoryFactory()(params={"cursor": cursor_})
    worker_ = RabbitMQGameWorkerFactory()(params={"repository": repository})
    main(worker_, connection_, cursor_)
