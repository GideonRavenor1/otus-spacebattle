from _pytest.logging import LogCaptureFixture

from src.dependencies import container
from src.exceptions import SetPositionException
from src.handlers import ExceptionHandler
from src.vectors import Vector
from tests.utils import get_game_object


def test_exception_handler_with_positive_scenario() -> None:
    """
    Проверяем, что обработчик ошибок запускает repeat команду и сдвигает объект с места.
    """

    handler = ExceptionHandler()
    mock_obj = {"position": Vector(12, 5), "velocity": Vector(-7, 3)}
    mock_movable_obj = get_game_object(data=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = container.resolve("command.move", params=move_params)

    handler.handle(command, SetPositionException("Объект не сдвинулся с места"))

    assert mock_movable_obj.get_position() == Vector(5, 8)


def test_exception_handler_with_negative_scenario(caplog: LogCaptureFixture) -> None:
    """
    Проверяем, что в лог выводится сообщение об ошибке
    """

    handler = ExceptionHandler()
    mock_obj = {"position": Vector(12, 5), "velocity": Vector(0, 0)}
    mock_movable_obj = get_game_object(data=mock_obj)
    move_params = {"obj": mock_movable_obj}
    command = container.resolve("command.move", params=move_params)

    handler.handle(command, SetPositionException("Объект не сдвинулся с места"))

    assert "Объект не сдвинулся с места" in caplog.text
