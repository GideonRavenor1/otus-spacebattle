from queue import Queue

from src.dependencies import container
from src.vectors import Vector


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

    mock_space_ship_obj = container.resolve("game.objects.create", params=mock_obj)
    params = {"obj": mock_space_ship_obj}

    forward_command = container.resolve("command.forward", params=params)
    hard_stop_command = container.resolve("command.hard_stop", params=params)
    forward_rotate_command = container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, hard_stop_command, forward_rotate_command]

    queue = container.resolve("command.get_queue", params={"queue": Queue()}).execute()
    for command in commands:
        queue.put(command)

    thread_command = container.resolve("command.to_thread", params={"queue": queue})
    thread_command.execute()
    thread_command.thread.join()

    assert mock_space_ship_obj.get_position() == Vector(5, 8)
    assert mock_space_ship_obj.get_fuel_level() == 90
    assert mock_space_ship_obj.get_velocity() == Vector(-7, 3)
