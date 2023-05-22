from src.game.consumers.base import BaseConsumer
from src.game.consumers.rabbitmq import RabbitMQConsumer


def main(consumer: BaseConsumer) -> None:
    consumer.start_consuming()
    consumer.close()


if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    main(consumer)
