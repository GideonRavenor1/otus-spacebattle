from _pytest.logging import LogCaptureFixture

from src.factories import COMMAND_FACTORIES


def test_logging_command(caplog: LogCaptureFixture) -> None:
    """
    Проверяем, что в консоль выводится сообщение об ошибке
    """

    exception = TypeError("Ошибка при выполнении команды")
    params = {"exception": exception}

    command = COMMAND_FACTORIES["log_exception"].create(params=params)
    command.execute()
    assert "Ошибка при выполнении команды" in caplog.text
