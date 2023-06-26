import random
from queue import Queue

import pytest

from src.game.dependencies.command_container import command_container
from src.game.dependencies.game_objects_container import game_container
from src.interpreter import CommandInterpreter


def test_interpret_valid_params() -> None:
    user_id = random.randint(1, 100)
    mock_obj = {
        "position": [12, 5],
        "velocity": [0, 0],
        "fuel_level": 100,
        "required_fuel_level": 10,
        "user_id": user_id,
    }

    mock_burning_fuel_obj = game_container.resolve("game.objects.create.object", params=mock_obj)

    queue = command_container.resolve(
        "command.get_queue",
        params={"queue": Queue(), "game_id": mock_burning_fuel_obj.get_id()},
    ).execute()

    interpreter = CommandInterpreter(
        ioc_container=command_container,
        game_object=mock_burning_fuel_obj,
        game_queue=queue,
        command_name="command.forward",
        user_id=user_id,
    )
    try:
        interpreter.interpret()
    except Exception as e:
        pytest.fail(e)
