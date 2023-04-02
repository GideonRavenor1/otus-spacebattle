import logging
from pathlib import Path

current_dir = Path(__file__).parent.resolve()

logger = logging.getLogger("exception_logger")

logFileFormatter = logging.Formatter(
    fmt="%(levelname)s %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(
    filename=current_dir / "logger.log",
)
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)

logger.addHandler(fileHandler)
