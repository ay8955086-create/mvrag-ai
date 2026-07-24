"""
Centralized logging configuration for MVRAG AI.

Every module in the project should obtain its logger using
`get_logger(__name__)` instead of configuring logging independently.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Lock

from src.config.settings import settings
from src.core.constants import (
    LOGGER_NAME,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    MAX_LOG_FILE_SIZE,
    LOG_BACKUP_COUNT,
)


class LoggerManager:
    """
    Creates and manages application loggers.

    Features
    --------
    - Singleton logger instances
    - Rotating log files
    - Console logging
    - Thread-safe initialization
    - Prevents duplicate handlers
    """

    _loggers: dict[str, logging.Logger] = {}
    _lock = Lock()

    @classmethod
    def get_logger(cls, name: str = LOGGER_NAME) -> logging.Logger:
        """
        Return a configured logger.

        Parameters
        ----------
        name : str
            Logger name.

        Returns
        -------
        logging.Logger
        """

        if name in cls._loggers:
            return cls._loggers[name]

        with cls._lock:
            if name in cls._loggers:
                return cls._loggers[name]

            logger = logging.getLogger(name)
            logger.setLevel(settings.LOG_LEVEL.upper())
            logger.propagate = False

            if logger.handlers:
                logger.handlers.clear()

            formatter = logging.Formatter(
                fmt=LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT,
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            log_file = Path(settings.logs_dir) / settings.LOG_FILE

            file_handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=MAX_LOG_FILE_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)

            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

            cls._loggers[name] = logger

            return logger


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """
    Convenience function for retrieving a logger.

    Example
    -------
    >>> logger = get_logger(__name__)
    >>> logger.info("Application started")
    """
    return LoggerManager.get_logger(name)


# Default application logger
logger = get_logger()