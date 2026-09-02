"""
Shared SQLAlchemy ORM mixins for MVRAG AI.

This module provides reusable mixins for primary keys and timestamps.
Every ORM model should inherit from these mixins.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    """
    Provides an auto-incrementing integer primary key.
    """

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


class TimestampMixin:
    """
    Provides created_at and updated_at timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseModel(PrimaryKeyMixin, TimestampMixin):
    """
    Base mixin combining primary key and timestamps.

    Inherit from this class together with the SQLAlchemy Base:

    Example
    -------
    class Video(Base, BaseModel):
        ...
    """