import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: int = logging.DEBUG, log_file: str = 'logging/app.log') -> logging.Logger:
    """
    Sets up the logging configuration.

    Args:
        log_level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
        log_file (str): The file where logs should be stored.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('app_logger')
    logger.setLevel(log_level)

    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=3)
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
