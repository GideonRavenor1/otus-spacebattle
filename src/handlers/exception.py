from src.commands import (
    BaseCommand,
    BaseMacroCommand,
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    ExceptionLoggingCommand,
    MoveCommand,
    FirstRepeatCommand,
    SecondRepeatCommand,
    RotateCommand,
    ForwardMacroCommand,
    ForwardWithRotateMacroCommand,
)
from src.exceptions import (
    NoFuelException,
    RaedDirectionNumberException,
    ReadAngularVelocityException,
    ReadDirectionException,
    ReadFuelLevelException,
    ReadPositionException,
    ReadRequiredFuelLevelException,
    ReadVelocityException,
    RepeatException,
    SetDirectionException,
    SetFuelLevelException,
    SetPositionException,
    SetVelocityException,
)
from src.handlers.base import BaseHandler

ROTATE_EXCEPTIONS = {
    ReadDirectionException: FirstRepeatCommand,
    ReadAngularVelocityException: FirstRepeatCommand,
    SetDirectionException: FirstRepeatCommand,
    RaedDirectionNumberException: FirstRepeatCommand,
}

MOVE_EXCEPTIONS = {
    ReadPositionException: FirstRepeatCommand,
    SetPositionException: FirstRepeatCommand,
    ReadVelocityException: FirstRepeatCommand,
}

CHANGE_VELOCITY_EXCEPTIONS = {
    ReadVelocityException: FirstRepeatCommand,
    SetVelocityException: FirstRepeatCommand,
}

CHECK_FUEL_EXCEPTIONS = {
    NoFuelException: FirstRepeatCommand,
    ReadRequiredFuelLevelException: FirstRepeatCommand,
    SetFuelLevelException: FirstRepeatCommand,
    ReadFuelLevelException: FirstRepeatCommand,
}

BURN_FUEL_EXCEPTIONS = {
    ReadRequiredFuelLevelException: FirstRepeatCommand,
    SetFuelLevelException: FirstRepeatCommand,
    ReadFuelLevelException: FirstRepeatCommand,
}

MACRO_COMMANDS_EXCEPTIONS = {
    **CHANGE_VELOCITY_EXCEPTIONS,
    **CHECK_FUEL_EXCEPTIONS,
    **BURN_FUEL_EXCEPTIONS,
    **MOVE_EXCEPTIONS,
    **ROTATE_EXCEPTIONS,
}

FIRST_REPEAT_EXCEPTIONS = {
    RepeatException: SecondRepeatCommand,
}

SECOND_REPEAT_EXCEPTIONS = {
    RepeatException: ExceptionLoggingCommand,
}

COMMANDS = {
    ChangeVelocityCommand: CHANGE_VELOCITY_EXCEPTIONS,
    CheckFuelCommand: CHECK_FUEL_EXCEPTIONS,
    BurnFuelCommand: BURN_FUEL_EXCEPTIONS,
    MoveCommand: MOVE_EXCEPTIONS,
    RotateCommand: ROTATE_EXCEPTIONS,
    BaseMacroCommand: MACRO_COMMANDS_EXCEPTIONS,
    ForwardMacroCommand: MACRO_COMMANDS_EXCEPTIONS,
    ForwardWithRotateMacroCommand: MACRO_COMMANDS_EXCEPTIONS,
    FirstRepeatCommand: FIRST_REPEAT_EXCEPTIONS,
    SecondRepeatCommand: SECOND_REPEAT_EXCEPTIONS,
}


class ExceptionHandler(BaseHandler):
    def handle(self, command: BaseCommand, exception: Exception) -> None:
        exception_type = type(exception.__cause__) if exception.__cause__ is not None else type(exception)
        command_type = type(command)
        handler_command = COMMANDS[command_type][exception_type](command=command, exception=exception)  # noqa

        try:
            handler_command.execute()
        except Exception as e:
            self.handle(handler_command, e)
