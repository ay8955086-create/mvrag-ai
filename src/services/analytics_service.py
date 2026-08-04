"""
Analytics service for MVRAG AI.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.chunk import Chunk
from src.models.video import Video


class AnalyticsService:

    @staticmethod
    def get_dashboard(db: Session) -> dict:

        total_videos = db.query(Video).count()

        total_chunks = db.query(Chunk).count()

        completed = (
            db.query(Video)
            .filter(Video.status == "Completed")
            .count()
        )

        processing = (
            db.query(Video)
            .filter(Video.status == "Processing")
            .count()
        )

        failed = (
            db.query(Video)
            .filter(Video.status == "Failed")
            .count()
        )

        return {
            "total_videos": total_videos,
            "total_chunks": total_chunks,
            "completed": completed,
            "processing": processing,
            "failed": failed,
        }