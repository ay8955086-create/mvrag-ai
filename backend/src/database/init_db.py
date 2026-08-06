"""
Database initialization utilities for MVRAG AI.

This module is responsible for creating database tables and
verifying database connectivity during application startup.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.core.logger import get_logger
from src.database.base import Base, engine

logger = get_logger(__name__)


def initialize_database() -> None:
    """
    Create all database tables defined by ORM models.
    Safe to call multiple times.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")

    except SQLAlchemyError as exc:
        logger.exception("Failed to initialize database.")
        raise exc


def check_database_connection() -> bool:
    """
    Verify that the database connection is working.

    Returns
    -------
    bool
        True if the connection succeeds.

    Raises
    ------
    SQLAlchemyError
        If the connection cannot be established.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database connection verified.")
        return True

    except SQLAlchemyError as exc:
        logger.exception("Database connection failed.")
        raise exc