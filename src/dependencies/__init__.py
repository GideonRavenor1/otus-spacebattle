from src.dependencies.containers import IoCContainer
from src.factories import (
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
)

container = IoCContainer()

container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.forward", "obj": ForwardMacroCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.forward_with_rotate", "obj": ForwardWithRotateCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.check_fuel", "obj": CheckFuelCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.burn_fuel", "obj": BurnFuelCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.first_repeat", "obj": FirstRepeatCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.second_repeat", "obj": SecondRepeatCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.rotate", "obj": RotateCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.move", "obj": MoveCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.change_velocity", "obj": ChangeVelocityCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.log_exception", "obj": ExceptionLoggingCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.soft_stop", "obj": SoftStopCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.hard_stop", "obj": HardStopCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.to_thread", "obj": ThreadCommandFactory()},
)
container.resolve(
    object_name="ioc.register",
    params={"obj_name": "command.get_queue", "obj": QueueCommandFactory()},
)
