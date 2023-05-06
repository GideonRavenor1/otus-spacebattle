from src.consumers.base import BaseConsumer
from src.consumers.rabbitmq import RabbitMQConsumer


def main(consumer: BaseConsumer) -> None:
    consumer.start_consuming()
    consumer.close()


if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    main(consumer)
