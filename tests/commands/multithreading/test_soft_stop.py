from queue import Queue

from src.dependencies import container
from src.vectors import Vector


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

    mock_space_ship_obj = container.resolve("game.objects.create", params=mock_obj)
    params = {"obj": mock_space_ship_obj}

    forward_command = container.resolve("command.forward", params=params)
    hard_stop_command = container.resolve("command.soft_stop", params=params)
    forward_rotate_command = container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, hard_stop_command, forward_rotate_command]

    queue = container.resolve("command.get_queue", params={"queue": Queue()}).execute()
    for command in commands:
        queue.put(command)

    thread_command = container.resolve("command.to_thread", params={"queue": queue})
    thread_command.execute()

    assert mock_space_ship_obj.get_position() == Vector(-2, 11)
    assert mock_space_ship_obj.get_fuel_level() == 70
    assert mock_space_ship_obj.get_velocity() == Vector(90, 210)
