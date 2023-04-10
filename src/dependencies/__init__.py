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
)

container = IoCContainer()

container.resolve(object_name="register", params={"obj_name": "forward", "obj": ForwardMacroCommandFactory()})
container.resolve(
    object_name="register",
    params={"obj_name": "forward_with_rotate", "obj": ForwardWithRotateCommandFactory()},
)
container.resolve(object_name="register", params={"obj_name": "check_fuel", "obj": CheckFuelCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "burn_fuel", "obj": BurnFuelCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "first_repeat", "obj": FirstRepeatCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "second_repeat", "obj": SecondRepeatCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "rotate", "obj": RotateCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "move", "obj": MoveCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "change_velocity", "obj": ChangeVelocityCommandFactory()})
container.resolve(object_name="register", params={"obj_name": "log_exception", "obj": ExceptionLoggingCommandFactory()})
