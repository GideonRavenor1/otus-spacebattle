from src.game.dependencies.containers import IoCContainer
from src.game.factories import (
    BurnFuelCommandFactory,
    ChangeVelocityCommandFactory,
    CheckFuelCommandFactory,
    ExceptionLoggingCommandFactory,
    FirstRepeatCommandFactory,
    ForwardMacroCommandFactory,
    ForwardWithRotateCommandFactory,
    MoveCommandFactory,
    RotateCommandFactory,
    SecondRepeatCommandFactory,
    SoftStopCommandFactory,
    ThreadCommandFactory,
    QueueCommandFactory,
    HardStopCommandFactory,
    GameObjectFactory,
    InterpretCommandFactory,
)

container = IoCContainer()

container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.forward", "obj": ForwardMacroCommandFactory(), "object_map_name": "forward"},
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.forward_with_rotate",
        "obj": ForwardWithRotateCommandFactory(),
        "object_map_name": "forward_with_rotate",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.check_fuel",
        "obj": CheckFuelCommandFactory(),
        "object_map_name": "check_fuel",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.burn_fuel",
        "obj": BurnFuelCommandFactory(),
        "object_map_name": "burn_fuel",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.first_repeat",
        "obj": FirstRepeatCommandFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.second_repeat",
        "obj": SecondRepeatCommandFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.rotate",
        "obj": RotateCommandFactory(),
        "object_map_name": "rotate",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.move",
        "obj": MoveCommandFactory(),
        "object_map_name": "move",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.change_velocity",
        "obj": ChangeVelocityCommandFactory(),
        "object_map_name": "change_velocity",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.log_exception",
        "obj": ExceptionLoggingCommandFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.soft_stop",
        "obj": SoftStopCommandFactory(),
        "object_map_name": "soft_stop",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.hard_stop",
        "obj": HardStopCommandFactory(),
        "object_map_name": "hard_stop",
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.to_thread",
        "obj": ThreadCommandFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.get_queue",
        "obj": QueueCommandFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "game.objects.create",
        "obj": GameObjectFactory(),
        "object_map_name": None,
    },
)
container.resolve(
    object_name="ioc.register",
    params={
        "obj_name": "command.interpret",
        "obj": InterpretCommandFactory(),
        "object_map_name": None,
    },
)
