"""
Database engine and declarative base for MVRAG AI.

This module initializes the SQLAlchemy engine and provides the
shared declarative base for all ORM models.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase

from src.config.settings import settings


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every database model in the project must inherit from this class.
    """


def create_database_engine() -> Engine:
    """
    Create and configure the SQLAlchemy engine.

    Returns
    -------
    Engine
        Configured SQLAlchemy engine.
    """
    return create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,
    )


# Singleton engine used throughout the application.
engine: Engine = create_database_engine()