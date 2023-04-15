class CommandException(Exception):
    """Ошибка при выполнении команды"""


class RepeatException(Exception):
    """Ошибка при повторном выполнении команды"""


class RegisterCommandException(Exception):
    """Ошибка при регистрации объекта"""


class ResolveDependencyException(Exception):
    """Ошибка при разрешении зависимости"""
