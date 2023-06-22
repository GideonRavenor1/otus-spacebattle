from src.game.commands.check_collision import CheckMapCollisionCommand
from src.game.commands.interpret import InterpretCommand
from src.game.commands.loggers import ExceptionLoggingCommand
from src.game.commands.macro_commands import ForwardMacroCommand, ForwardWithRotateMacroCommand
from src.game.commands.move import ChangeVelocityCommand, MoveCommand
from src.game.commands.repeats import SecondRepeatCommand, FirstRepeatCommand
from src.game.commands.rotate import RotateCommand
from src.game.commands.multithreading import (
    QueueCommand,
    HardStopCommand,
    SoftStopCommand,
    ThreadCommand,
    MoveToCommand,
    RunCommand,
)
from src.game.commands.register import RegisterObject
from src.game.commands.fuel_dependent import BurnFuelCommand, CheckFuelCommand
