from _pytest.logging import LogCaptureFixture

from src.dependencies import container
from src.managers import QueueManager
from src.vectors import Vector
from tests.utils import get_game_object


def test_queue_manager_with_valid_params() -> None:
    mock_obj = {
        "position": Vector(12, 5),
        "velocity": Vector(-7, 3),
        "fuel_level": 100,
        "required_fuel_level": 10,
        "direction": 100,
        "angular_velocity": 30,
        "direction_number": 360,
    }

    mock_space_ship_obj = get_game_object(data=mock_obj)
    params = {"obj": mock_space_ship_obj}
    forward_command = container.resolve("command.forward", params=params)
    forward_rotate_command = container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, forward_rotate_command]
    manager = QueueManager(commands=commands)
    manager.run()

    assert mock_space_ship_obj.get_position() == Vector(-2, 11)
    assert mock_space_ship_obj.get_fuel_level() == 70
    assert mock_space_ship_obj.get_velocity() == Vector(90, 210)


def test_manager_with_not_enough_fuel(caplog: LogCaptureFixture) -> None:
    """
    Проверка на то, что топливо кончится после отработки первой макрокоманды, и вторая не выполнится.
    Так же проверяем, что ошибка записалось в лог.
    """

    mock_obj = {
        "position": Vector(12, 5),
        "velocity": Vector(-7, 3),
        "fuel_level": 20,
        "required_fuel_level": 10,
        "direction": 100,
        "angular_velocity": 30,
        "direction_number": 360,
    }

    mock_space_ship_obj = get_game_object(data=mock_obj)
    params = {"obj": mock_space_ship_obj}
    forward_command = container.resolve("command.forward", params=params)
    forward_rotate_command = container.resolve("command.forward_with_rotate", params=params)

    commands = [forward_command, forward_rotate_command]
    manager = QueueManager(commands=commands)
    manager.run()

    assert mock_space_ship_obj.get_position() == Vector(-2, 11)
    assert mock_space_ship_obj.get_fuel_level() == 0
    assert mock_space_ship_obj.get_velocity() == Vector(-7, 3)
    assert "Недостаточно топлива" in caplog.text
