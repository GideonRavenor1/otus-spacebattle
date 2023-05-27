import json
from sqlite3 import Cursor

import pika
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from src.game.workers.base import BaseWorker
from src.game.dispatchers.base import Dispatcher
from src.logger.settings import logger
from src.config import get_settings

settings = get_settings()


class RabbitMQGameWorker(BaseWorker):
    URL = settings.AMQP_URL
    CLIENT_QUEUE = settings.CLIENT_QUEUE
    GAME_QUEUE = settings.GAME_QUEUE
    AUTH_QUEUE = settings.AUTH_QUEUE

    def __init__(self, cursor: Cursor) -> None:
        parameters = pika.URLParameters(self.URL)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.GAME_QUEUE)
        self.channel.queue_declare(queue=self.AUTH_QUEUE)
        self.channel.queue_declare(queue=self.CLIENT_QUEUE)
        self._dispatcher = Dispatcher(cursor=cursor)

    def start_consuming(self) -> None:
        def callback(
            ch: BlockingChannel,  # noqa
            method: Basic.Deliver,  # noqa
            properties: BasicProperties,  # noqa
            body: bytes,
        ) -> None:
            message = json.loads(body)
            action = message.pop("action", None)
            logger.info(f"Received Game message: {message}, action: {action}")
            if action is None:
                return

            try:
                result = self._dispatcher.dispatch(
                    action=action,
                    params=message,
                    auth_queue=self.AUTH_QUEUE,
                    channel=self.channel,
                )
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                result = {"error": str(e), "action": action}

            self.channel.basic_publish(
                exchange="",
                routing_key=self.CLIENT_QUEUE,
                body=json.dumps(result).encode("utf-8"),
            )

        self.channel.basic_consume(queue=self.GAME_QUEUE, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self) -> None:
        self.channel.close()
        self.connection.close()
