from src.authentication.workers.base import BaseWorker
from src.authentication.workers.rabbitmq import RabbitMQAuthWorker


def main(worker: BaseWorker) -> None:
    try:
        worker.start_consuming()
    finally:
        worker.close()


if __name__ == "__main__":
    worker_ = RabbitMQAuthWorker()
    main(worker_)
