import random

from _pytest.logging import LogCaptureFixture

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.managers import QueueManager
from src.game.vectors import Vector


def test_queue_manager_with_valid_params() -> None:
    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [-7, 3],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "direction": 100,
        "angular_velocity": 30,
        "direction_number": 360,
        "user_id": user_id,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}
    forward_command = command_container.resolve("command.forward", params=params)
    forward_rotate_command = command_container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, forward_rotate_command]
    manager = QueueManager(commands=commands)
    manager.run()

    assert mock_space_ship_obj.get_position() == Vector(-2, 11, mock_space_ship_obj.get_id())
    assert mock_space_ship_obj.get_fuel_level() == 70
    assert mock_space_ship_obj.get_velocity() == Vector(90, 210, mock_space_ship_obj.get_id())


def test_manager_with_not_enough_fuel(caplog: LogCaptureFixture) -> None:
    """
    Проверка на то, что топливо кончится после отработки первой макрокоманды, и вторая не выполнится.
    Так же проверяем, что ошибка записалось в лог.
    """

    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [-7, 3],
        "fuel_level": 20,
        "required_fuel_level": 10,
        "direction": 100,
        "angular_velocity": 30,
        "direction_number": 360,
        "user_id": user_id,
    }

    mock_space_ship_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    params = {"obj": mock_space_ship_obj}
    forward_command = command_container.resolve("command.forward", params=params)
    forward_rotate_command = command_container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, forward_rotate_command]
    manager = QueueManager(commands=commands)
    manager.run()

    assert mock_space_ship_obj.get_position() == Vector(-2, 11, mock_space_ship_obj.get_id())
    assert mock_space_ship_obj.get_fuel_level() == 0
    assert mock_space_ship_obj.get_velocity() == Vector(-7, 3, mock_space_ship_obj.get_id())
    assert "Недостаточно топлива" in caplog.text
