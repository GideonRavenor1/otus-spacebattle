import random

from _pytest.logging import LogCaptureFixture

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import SetPositionException
from src.game.handlers import ExceptionHandler
from src.game.vectors import Vector


def test_exception_handler_with_positive_scenario() -> None:
    """
    Проверяем, что обработчик ошибок запускает repeat команду и сдвигает объект с места.
    """
    user_id = random.randint(1, 100)
    handler = ExceptionHandler()
    mock_obj = {"position": [12, 5], "velocity": [-7, 3], "user_id": user_id}
    mock_movable_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = command_container.resolve("command.move", params=move_params)

    handler.handle(command, SetPositionException("Объект не сдвинулся с места"))

    assert mock_movable_obj.get_position() == Vector(5, 8, mock_movable_obj.get_id())


def test_exception_handler_with_negative_scenario(caplog: LogCaptureFixture) -> None:
    """
    Проверяем, что в лог выводится сообщение об ошибке
    """

    user_id = random.randint(1, 100)
    handler = ExceptionHandler()
    mock_obj = {"position": [12, 5], "velocity": [0, 0], "user_id": user_id}
    mock_movable_obj = game_container.resolve("game.objects.create.object", params=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = command_container.resolve("command.move", params=move_params)

    handler.handle(command, SetPositionException("Объект не сдвинулся с места"))

    assert "Объект не сдвинулся с места" in caplog.text
