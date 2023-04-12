import logging
from pathlib import Path

current_dir = Path(__file__).parent.resolve()


def get_logger() -> logging.Logger:
    logger_ = logging.getLogger("exception_logger")

    formatter = logging.Formatter(
        fmt="%(levelname)s %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(
        filename=current_dir / "logger.log",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level=logging.INFO)

    logger_.addHandler(file_handler)
    return logger_


logger = get_logger()
