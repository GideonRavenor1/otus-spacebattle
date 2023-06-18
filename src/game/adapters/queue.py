from queue import Queue

from src.game.commands.base import BaseCommand


class QueueAdapter:
    def __init__(self, queue: Queue, game_id: str) -> None:
        self._queue = queue
        self._game_id = game_id

    def get(self, timeout: float | None = None) -> BaseCommand:
        return self._queue.get(timeout=timeout)

    def get_game_id(self) -> str:
        return self._game_id

    def task_done(self) -> None:
        self._queue.task_done()

    def put(self, command: BaseCommand) -> None:
        self._queue.put(command)

    def is_empty(self) -> bool:
        return self._queue.empty()
