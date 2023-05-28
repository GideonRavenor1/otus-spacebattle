import json

import pika
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from src.authentication.dispatchers.base import Dispatcher
from src.authentication.workers.base import BaseWorker
from src.logger import logger
from src.config import get_settings

settings = get_settings()


class RabbitMQAuthWorker(BaseWorker):
    URL = settings.AMQP_URL
    AUTH_QUEUE = settings.AUTH_QUEUE
    GAME_QUEUE = settings.GAME_QUEUE

    def __init__(self) -> None:
        parameters = pika.URLParameters(self.URL)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self._dispatcher = Dispatcher()

    def start_consuming(self) -> None:
        def callback(
            ch: BlockingChannel,  # noqa
            method: Basic.Deliver,  # noqa
            properties: BasicProperties,  # noqa
            body: bytes,
        ) -> None:
            message = json.loads(body)
            action = message.pop("action", None)
            logger.info(f"Received Auth message: {message}, action: {action}")
            if action is None:
                return
            try:
                result = self._dispatcher.dispatch(action=action, params=message)
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                result = {"error": str(e), "action": action}

            self.channel.basic_publish(
                exchange="",
                routing_key=self.GAME_QUEUE,
                body=json.dumps(result).encode("utf-8"),
            )

        self.channel.basic_consume(queue=self.AUTH_QUEUE, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self) -> None:
        self.channel.close()
        self.connection.close()
