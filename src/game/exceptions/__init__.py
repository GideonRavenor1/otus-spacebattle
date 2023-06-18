from src.game.exceptions.auth import AuthenticationException
from src.game.exceptions.command import (
    CommandException,
    RegisterObjectException,
    RepeatException,
    ResolveDependencyException,
)
from src.game.exceptions.fuel_dependent import (
    NoFuelException,
    ReadFuelLevelException,
    ReadRequiredFuelLevelException,
    SetFuelLevelException,
)
from src.game.exceptions.game_map import (
    OutOfMapRangeException,
    PositionOccupiedException,
    ObjectsCollided,
)
from src.game.exceptions.move import (
    ReadPositionException,
    ReadVelocityException,
    SetPositionException,
    SetVelocityException,
)
from src.game.exceptions.rotate import (
    RaedDirectionNumberException,
    ReadAngularVelocityException,
    ReadDirectionException,
    SetDirectionException,
)
