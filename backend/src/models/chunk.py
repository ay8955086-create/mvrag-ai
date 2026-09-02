"""
Chunk ORM model for MVRAG AI.

Stores semantic chunks created from video transcripts, OCR results,
and AI-generated captions. Each chunk corresponds to a segment of
the video and is linked to an embedding stored in ChromaDB.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.video import Video


class Chunk(Base, BaseModel):
    """
    Represents a semantic chunk used by the RAG pipeline.
    """

    __tablename__ = "chunks"

    __table_args__ = (
        Index("idx_chunk_video_id", "video_id"),
        Index("idx_chunk_embedding_id", "embedding_id"),
        Index("idx_chunk_timestamp", "start_time", "end_time"),
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Chunk Metadata
    # ------------------------------------------------------------------

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    end_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    ocr_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    caption: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    combined_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Embedding Information
    # ------------------------------------------------------------------

    embedding_id: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
    unique=True,
)

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    video: Mapped["Video"] = relationship(
        back_populates="chunks",
    )

    def __repr__(self) -> str:
        return (
            f"Chunk("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"chunk_index={self.chunk_index}, "
            f"start={self.start_time:.2f}, "
            f"end={self.end_time:.2f})"
        )