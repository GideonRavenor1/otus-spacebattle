from queue import Queue

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.handlers.state import CommandProcessor
from src.game.vectors import Vector


def test_hard_stop_with_valid_params() -> None:
    """
    В данном тесты мы проверяем, что отработает лишь первая макрокоманда "forward", после чего сработает
    "hard_stop", которая остановит исполнение очереди и потока.
    """

    mock_obj = {
        "position": [12, 5],
        "velocity": [-7, 3],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "direction": 100,
        "angular_velocity": 30,
        "direction_number": 360,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}

    forward_command = command_container.resolve("command.forward", params=params)
    hard_stop_command = command_container.resolve("command.hard_stop", params=params)
    forward_rotate_command = command_container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, hard_stop_command, forward_rotate_command]

    queue = command_container.resolve(
        "command.get_queue",
        params={"queue": Queue(), "game_id": mock_space_ship_obj.get_id()},
    ).execute()
    for command in commands:
        queue.put(command)

    command_processor = CommandProcessor(queue)
    thread_command = command_container.resolve("command.to_thread", params={"command_processor": command_processor})
    thread_command.execute()
    thread_command.thread.join()

    assert mock_space_ship_obj.get_position() == Vector(5, 8, mock_space_ship_obj.get_id())
    assert mock_space_ship_obj.get_fuel_level() == 90
    assert mock_space_ship_obj.get_velocity() == Vector(-7, 3, mock_space_ship_obj.get_id())
