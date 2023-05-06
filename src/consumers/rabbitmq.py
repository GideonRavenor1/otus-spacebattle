import json

import pika
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from src.consumers.base import BaseConsumer
from src.dispatchers.base import Dispatcher
from src.logger.settings import logger


class RabbitMQConsumer(BaseConsumer):
    _dispatcher = Dispatcher()

    URL = "amqp://localhost:5672/"

    def __init__(self) -> None:
        parameters = pika.URLParameters(self.URL)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def start_consuming(self) -> None:
        def callback(
            ch: BlockingChannel,  # noqa
            method: Basic.Deliver,  # noqa
            properties: BasicProperties,  # noqa
            body: bytes,
        ) -> None:
            message = json.loads(body)
            action = message.pop("action", None)
            logger.info(f"Received message: {message}, action: {action}")
            if action is None:
                return
            try:
                self._dispatcher.dispatch(action=action, params=message)
            except Exception as e:
                logger.error(f"Ошибка: {e}")

        self.channel.basic_consume(queue="otus-queue", on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self) -> None:
        self.channel.close()
        self.connection.close()
