"""
Caption ORM model for MVRAG AI.

Stores AI-generated image captions for video frames.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.video import Video


class Caption(Base, BaseModel):
    """
    Represents an AI-generated caption for a video frame.
    """

    __tablename__ = "captions"

    __table_args__ = (
        Index("idx_caption_video_id", "video_id"),
        Index("idx_caption_timestamp", "timestamp"),
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Caption Information
    # ------------------------------------------------------------------

    frame_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    timestamp: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    caption: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    video: Mapped["Video"] = relationship(
        back_populates="captions",
    )

    def __repr__(self) -> str:
        return (
            f"Caption("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"frame={self.frame_number}, "
            f"timestamp={self.timestamp})"
        )