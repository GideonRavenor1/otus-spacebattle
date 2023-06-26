import random
from queue import Queue

import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.game.exceptions import PermissionException
from src.interpreter import CommandInterpreter


def test_interpret_invalid_params() -> None:
    user_id_1 = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [0, 0],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "user_id": user_id_1,
    }

    mock_burning_fuel_obj = game_container.resolve("game.objects.create.object", params=mock_obj)

    queue = command_container.resolve(
        "command.get_queue",
        params={"queue": Queue(), "game_id": mock_burning_fuel_obj.get_id()},
    ).execute()

    user_id_2 = random.randint(100, 200)

    with pytest.raises(PermissionException):
        CommandInterpreter(
            ioc_container=command_container,
            game_object=mock_burning_fuel_obj,
            game_queue=queue,
            command_name="command.forward",
            user_id=user_id_2,
        ).interpret()
