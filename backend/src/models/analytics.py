"""
Analytics ORM model for MVRAG AI.

Stores processing statistics and performance metrics for each video.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.video import Video


class Analytics(Base, BaseModel):
    """
    Stores analytics generated during video processing.

    There is exactly one Analytics record for every Video.
    """

    __tablename__ = "analytics"

    __table_args__ = (
        Index("idx_analytics_video_id", "video_id"),
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # ------------------------------------------------------------------
    # Processing Statistics
    # ------------------------------------------------------------------

    processing_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    transcript_segments: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    ocr_detections: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    caption_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    total_queries: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    average_response_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    video: Mapped["Video"] = relationship(
        back_populates="analytics",
    )

    def __repr__(self) -> str:
        return (
            f"Analytics("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"processing_time={self.processing_time:.2f}s, "
            f"chunks={self.chunk_count})"
        )