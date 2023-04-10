from _pytest.logging import LogCaptureFixture

from src.dependencies import container


def test_logging_command(caplog: LogCaptureFixture) -> None:
    """
    Проверяем, что в консоль выводится сообщение об ошибке
    """

    exception = TypeError("Ошибка при выполнении команды")
    params = {"exception": exception}

    command = container["log_exception"](params=params)
    command.execute()
    assert "Ошибка при выполнении команды" in caplog.text
