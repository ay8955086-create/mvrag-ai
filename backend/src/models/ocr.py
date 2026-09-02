"""
OCR ORM model for MVRAG AI.

Stores text extracted from video frames using OCR.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.video import Video


class OCRResult(Base, BaseModel):
    """
    Represents OCR text extracted from a single video frame.
    """

    __tablename__ = "ocr_results"

    __table_args__ = (
        Index("idx_ocr_video_id", "video_id"),
        Index("idx_ocr_timestamp", "timestamp"),
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # OCR Information
    # ------------------------------------------------------------------

    frame_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    timestamp: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    video: Mapped["Video"] = relationship(
        back_populates="ocr_results",
    )

    def __repr__(self) -> str:
        return (
            f"OCRResult("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"frame={self.frame_number}, "
            f"timestamp={self.timestamp})"
        )