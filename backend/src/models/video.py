"""
Video ORM model for MVRAG AI.

This model represents an uploaded video and acts as the root entity
for all processing results such as transcripts, OCR, captions,
semantic chunks, user queries, and analytics.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.analytics import Analytics
    from src.models.caption import Caption
    from src.models.chunk import Chunk
    from src.models.ocr import OCRResult
    from src.models.query import Query
    from src.models.transcript import Transcript


class Video(Base, BaseModel):
    """
    Represents one uploaded video.

    One uploaded file corresponds to exactly one Video record.
    """

    __tablename__ = "videos"

    __table_args__ = (
        Index("idx_video_filename", "filename"),
        Index("idx_video_status", "status"),
        Index("idx_video_upload_time", "upload_time"),
    )

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Video Metadata
    # ------------------------------------------------------------------

    duration: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    fps: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    size_mb: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Pending",
    )

    upload_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    processed_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    transcripts: Mapped[list["Transcript"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    ocr_results: Mapped[list["OCRResult"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    captions: Mapped[list["Caption"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    queries: Mapped[list["Query"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    analytics: Mapped["Analytics | None"] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"Video(id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status}')"
        )