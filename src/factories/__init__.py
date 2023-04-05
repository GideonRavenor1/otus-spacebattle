from src.factories.macro_commands import ForwardMacroCommandFactory, ForwardWithRotateCommandFactory
from src.factories.fuel_dependent import CheckFuelCommandFactory, BurnFuelCommandFactory
from src.factories.repeats import FirstRepeatCommandFactory, SecondRepeatCommandFactory
from src.factories.rotate import RotateCommandFactory
from src.factories.base import BaseCommandFactory
from src.factories.move import MoveCommandFactory, ChangeVelocityCommandFactory
from src.factories.loggers import ExceptionLoggingCommandFactory


COMMAND_FACTORIES: dict[str, BaseCommandFactory] = {
    "forward": ForwardMacroCommandFactory(),
    "forward_with_rotate": ForwardWithRotateCommandFactory(),
    "check_fuel": CheckFuelCommandFactory(),
    "burn_fuel": BurnFuelCommandFactory(),
    "first_repeat": FirstRepeatCommandFactory(),
    "second_repeat": SecondRepeatCommandFactory(),
    "rotate": RotateCommandFactory(),
    "move": MoveCommandFactory(),
    "change_velocity": ChangeVelocityCommandFactory(),
    "log_exception": ExceptionLoggingCommandFactory(),
}
