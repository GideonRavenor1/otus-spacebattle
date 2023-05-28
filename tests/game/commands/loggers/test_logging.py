from _pytest.logging import LogCaptureFixture

from src.game.dependencies.command_container import command_container


def test_logging_command(caplog: LogCaptureFixture) -> None:
    """
    Проверяем, что в консоль выводится сообщение об ошибке
    """

    exception = TypeError("Ошибка при выполнении команды")
    params = {"exception": exception}

    command = command_container.resolve("command.log_exception", params=params)
    command.execute()
    assert "Ошибка при выполнении команды" in caplog.text
