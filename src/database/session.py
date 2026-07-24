from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session, sessionmaker

from src.database.base import engine


# -----------------------------------------------------------------------------
# Session Factory
# -----------------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# -----------------------------------------------------------------------------
# Dependency
# -----------------------------------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields
    ------
    Session
        Active SQLAlchemy session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# Context Manager
# -----------------------------------------------------------------------------

@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.

    Example
    -------
    >>> with session_scope() as session:
    ...     session.add(obj)
    """

    session = SessionLocal()

    try:
        yield session
        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()