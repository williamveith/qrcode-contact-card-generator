from .configs import *
import pathlib

LOG_LEVEL = logging.DEBUG
LOG_FILE = 'app.log'

ROOT_DIRECTORY = pathlib.Path(__file__).resolve().parent
log_file = ROOT_DIRECTORY / LOG_FILE
with log_file.open("w") as file:
    pass

log = configs.setup_logging(log_level=LOG_LEVEL, log_file=str(log_file))

__all__ = ["log"]