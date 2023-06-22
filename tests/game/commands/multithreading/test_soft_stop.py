from queue import Queue

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.handlers.state import CommandProcessor
from src.game.vectors import Vector


def test_soft_stop_with_valid_params() -> None:
    """
    В данном тесты мы проверяем, что отработает обе макрокоманды "forward", после чего поток остановится.
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
    soft_stop_command = command_container.resolve("command.soft_stop", params=params)
    forward_rotate_command = command_container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, soft_stop_command, forward_rotate_command]

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

    assert mock_space_ship_obj.get_position() == Vector(-2, 11, mock_space_ship_obj.get_id())
    assert mock_space_ship_obj.get_fuel_level() == 70
    assert mock_space_ship_obj.get_velocity() == Vector(90, 210, mock_space_ship_obj.get_id())
