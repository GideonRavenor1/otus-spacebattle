from abc import ABC
from typing import TYPE_CHECKING, NewType, Union
from queue import Empty, Queue

from src.game.commands import HardStopCommand, MoveToCommand, RunCommand, SoftStopCommand
from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.handlers import BaseHandler, ExceptionHandler

if TYPE_CHECKING:
    from src.game.adapters import QueueAdapter
    from src.game.commands.base import BaseCommand


STATE_RETURN_VALUE = NewType("NORMAL_STATE_RETURN_VALUE", Union[None, "MoveToState", "NormalState"])

HARD_STOP_COMMAND_NAME = HardStopCommand.__name__
SOFT_STOP_COMMAND_NAME = SoftStopCommand.__name__
MOVE_TO_COMMAND_NAME = MoveToCommand.__name__
RUN_COMMAND_NAME = RunCommand.__name__


class CommandProcessor:
    def __init__(self, command_queue: "QueueAdapter") -> None:
        self.command_queue = command_queue
        self.state = NormalState()

    def __call__(self, *args, **kwargs) -> None:
        self._process_commands()

    def _process_commands(self) -> None:
        while self.state is not None:
            self.state = self.state.handle(self.command_queue)

    @property
    def status(self) -> str:
        return type(self.state).__name__ if self.state is not None else "None"


class StateHandler(BaseHandler, ABC):
    _exception_handler = ExceptionHandler()

    def _execute_command(self, command: "BaseCommand", command_queue: "QueueAdapter") -> None:
        with command.lock:
            try:
                command.execute()
            except Exception as exception:
                self._exception_handler.handle(command, exception)
        command_queue.task_done()


class NormalState(StateHandler):
    def handle(self, command_queue: "QueueAdapter") -> STATE_RETURN_VALUE:
        states = {
            HARD_STOP_COMMAND_NAME: lambda: None,
            MOVE_TO_COMMAND_NAME: MoveToState,
            SOFT_STOP_COMMAND_NAME: SoftStopState,
        }
        try:
            command = command_queue.get(timeout=2)
        except Empty:
            return self

        command_name = type(command).__name__
        self._execute_command(command, command_queue)

        return states[command_name]() if command_name in states else self


class MoveToState(StateHandler):
    def handle(self, command_queue: "QueueAdapter") -> STATE_RETURN_VALUE:
        states = {
            HARD_STOP_COMMAND_NAME: lambda: None,
            RUN_COMMAND_NAME: NormalState,
        }
        game_id = command_queue.get_game_id()
        queue_command = command_container.resolve(
            "command.get_queue",
            params={"queue": Queue(), "game_id": game_id},
        ).execute()

        while not command_queue.is_empty():
            command = command_queue.get(timeout=2)
            command_name = type(command).__name__

            if command_name in states:
                return states[command_name]()

            queue_command.put(command)

        game_container.resolve(
            "ioc.register",
            params={
                "obj_name": f"game.neutral_queues.{game_id}",
                "obj": lambda params: queue_command,  # noqa
            },
        )
        return NormalState()


class SoftStopState(StateHandler):
    def handle(self, command_queue: "QueueAdapter") -> STATE_RETURN_VALUE:
        states = {
            HARD_STOP_COMMAND_NAME: lambda: None,
            RUN_COMMAND_NAME: NormalState,
        }

        while not command_queue.is_empty():
            command = command_queue.get()
            command_name = type(command).__name__

            self._execute_command(command, command_queue)

            if command_name in states:
                return states[command_name]()

        return None
