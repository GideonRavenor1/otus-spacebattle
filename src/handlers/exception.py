from src.commands import (
    BaseCommand,
    BaseMacroCommand,
    BurnFuelCommand,
    ChangeVelocityCommand,
    CheckFuelCommand,
    ExceptionLoggingCommand,
    MoveCommand,
    RepeatCommand,
    RotateCommand,
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
    ReadDirectionException: RepeatCommand,
    ReadAngularVelocityException: RepeatCommand,
    SetDirectionException: RepeatCommand,
    RaedDirectionNumberException: RepeatCommand,
}

MOVE_EXCEPTIONS = {
    ReadPositionException: RepeatCommand,
    SetPositionException: RepeatCommand,
    ReadVelocityException: RepeatCommand,
}

CHANGE_VELOCITY_EXCEPTIONS = {
    ReadVelocityException: RepeatCommand,
    SetVelocityException: RepeatCommand,
}

CHECK_FUEL_EXCEPTIONS = {
    NoFuelException: RepeatCommand,
    ReadRequiredFuelLevelException: RepeatCommand,
    SetFuelLevelException: RepeatCommand,
    ReadFuelLevelException: RepeatCommand,
}

BURN_FUEL_EXCEPTIONS = {
    ReadRequiredFuelLevelException: RepeatCommand,
    SetFuelLevelException: RepeatCommand,
    ReadFuelLevelException: RepeatCommand,
}

MACRO_COMMANDS_EXCEPTIONS = {
    **CHANGE_VELOCITY_EXCEPTIONS,
    **CHECK_FUEL_EXCEPTIONS,
    **BURN_FUEL_EXCEPTIONS,
    **MOVE_EXCEPTIONS,
    **ROTATE_EXCEPTIONS,
}

COMMANDS = {
    ChangeVelocityCommand: CHANGE_VELOCITY_EXCEPTIONS,
    CheckFuelCommand: CHECK_FUEL_EXCEPTIONS,
    BurnFuelCommand: BURN_FUEL_EXCEPTIONS,
    MoveCommand: MOVE_EXCEPTIONS,
    RotateCommand: ROTATE_EXCEPTIONS,
    BaseMacroCommand: MACRO_COMMANDS_EXCEPTIONS,
}


class ExceptionHandler(BaseHandler):
    def handle(self, command: BaseCommand, exception: Exception) -> None:
        exception_type = type(exception.__cause__) if exception.__cause__ is not None else type(exception)

        if exception_type is RepeatException:
            ExceptionLoggingCommand(exception).execute()
            return

        command_type = type(command)
        handler_command = COMMANDS[command_type][exception_type](command)

        try:
            handler_command.execute()
        except Exception as e:
            self.handle(handler_command, e)
