import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_DIR, LOG_FILE

os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)


def setup_logger():
    """
    Set up a logger with both console and file handlers.
    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # -------------------------------------------------
    # ROOT LOGGER
    # -------------------------------------------------
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # -------------------------------------------------
    # CONSOLE HANDLER
    # -------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add console handler to the logger
    logger.addHandler(console_handler)

    # -------------------------------------------------
    # FILE HANDLER
    # -------------------------------------------------
    file_handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    # Add file handler to the logger
    logger.addHandler(file_handler)
    
    return logger