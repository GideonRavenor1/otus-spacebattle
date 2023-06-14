from src.game.dependencies.base import IoCContainer
from src.game.factories import (
    BurnFuelCommandFactory,
    ChangeVelocityCommandFactory,
    CheckFuelCommandFactory,
    ExceptionLoggingCommandFactory,
    FirstRepeatCommandFactory,
    ForwardMacroCommandFactory,
    ForwardWithRotateMacroCommandFactory,
    MoveCommandFactory,
    RotateCommandFactory,
    SecondRepeatCommandFactory,
    SoftStopCommandFactory,
    ThreadCommandFactory,
    QueueCommandFactory,
    HardStopCommandFactory,
    InterpretCommandFactory,
    ForwardAndCheckCollisionMacroCommandFactory,
)

command_container = IoCContainer()


command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.forward_and_check_collision",
        "obj": ForwardAndCheckCollisionMacroCommandFactory(),
        "object_map_name": "forward",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.forward_with_rotate_and_check_collision",
        "obj": ForwardWithRotateMacroCommandFactory(),
        "object_map_name": "forward_with_rotate",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.forward",
        "obj": ForwardMacroCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.forward_with_rotate",
        "obj": ForwardWithRotateMacroCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.check_fuel",
        "obj": CheckFuelCommandFactory(),
        "object_map_name": "check_fuel",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.burn_fuel",
        "obj": BurnFuelCommandFactory(),
        "object_map_name": "burn_fuel",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.first_repeat",
        "obj": FirstRepeatCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.second_repeat",
        "obj": SecondRepeatCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.rotate",
        "obj": RotateCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.move",
        "obj": MoveCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.change_velocity",
        "obj": ChangeVelocityCommandFactory(),
        "object_map_name": "change_velocity",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.log_exception",
        "obj": ExceptionLoggingCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.soft_stop",
        "obj": SoftStopCommandFactory(),
        "object_map_name": "soft_stop",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.hard_stop",
        "obj": HardStopCommandFactory(),
        "object_map_name": "hard_stop",
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.to_thread",
        "obj": ThreadCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.get_queue",
        "obj": QueueCommandFactory(),
        "object_map_name": None,
    },
)
command_container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.interpret",
        "obj": InterpretCommandFactory(),
        "object_map_name": None,
    },
)
