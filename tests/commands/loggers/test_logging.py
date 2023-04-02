from src.commands import ExceptionLoggingCommand


def test_logging_command(caplog) -> None:
    """
    Проверяем, что в консоль выводится сообщение об ошибке
    """

    exception = TypeError("Ошибка при выполнении команды")
    command = ExceptionLoggingCommand(exception)
    command.execute()
    assert "Ошибка при выполнении команды" in caplog.text
