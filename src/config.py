import dataclasses
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.resolve() / ".env"

load_dotenv(dotenv_path=ENV_PATH)


@dataclasses.dataclass
class Settings:
    AMQP_URL: str
    CLIENT_QUEUE: str
    GAME_QUEUE: str
    AUTH_QUEUE: str
    AUTH_SECRET: str
    AUTH_ALGORITHM: str
    AUTH_DB: str
    AUTH_TABLE: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        AMQP_URL=os.getenv("AMQP_URL"),
        CLIENT_QUEUE=os.getenv("CLIENT_QUEUE"),
        GAME_QUEUE=os.getenv("GAME_QUEUE"),
        AUTH_QUEUE=os.getenv("AUTH_QUEUE"),
        AUTH_SECRET=os.getenv("AUTH_SECRET"),
        AUTH_ALGORITHM=os.getenv("AUTH_ALGORITHM"),
        AUTH_DB=os.getenv("AUTH_DB"),
        AUTH_TABLE=os.getenv("AUTH_TABLE"),
    )
