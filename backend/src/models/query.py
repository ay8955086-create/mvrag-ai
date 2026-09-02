"""
Query ORM model for MVRAG AI.

Stores every question asked by the user for a particular video along
with the generated answer and response metadata.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.video import Video


class Query(Base, BaseModel):
    """
    Represents a user query and the corresponding AI-generated answer.
    """

    __tablename__ = "queries"

    __table_args__ = (
        Index("idx_query_video_id", "video_id"),
        Index("idx_query_created_at", "created_at"),
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Query Information
    # ------------------------------------------------------------------

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    video: Mapped["Video"] = relationship(
        back_populates="queries",
    )

    def __repr__(self) -> str:
        return (
            f"Query("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"response_time={self.response_time:.2f}s)"
        )