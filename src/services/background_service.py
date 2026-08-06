"""
Background processing service for MVRAG AI.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.config.settings import settings
from src.core.logger import get_logger
from src.models.video import Video
from src.pipeline.video_pipeline import VideoPipeline

logger = get_logger(__name__)


class BackgroundService:
    """
    Executes long-running video processing tasks.
    """

    @staticmethod
    def process_video(
        db: Session,
        video_id: int,
    ) -> None:
        """
        Run the AI pipeline in the background.
        """

        logger.info(
            "Starting background processing for video %d",
            video_id,
        )

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            logger.error(
                "Video %d not found.",
                video_id,
            )
            return

        try:

            pipeline = VideoPipeline(
                db=db,
                video_id=video_id,
            )

            video_path = (
                settings.raw_video_dir
                / video.filename
            )

            pipeline.process(
                video_path,
            )

            video.status = "Completed"

            db.commit()

            logger.info(
                "Background processing completed successfully."
            )

        except Exception as error:

            logger.exception(
                "Background processing failed: %s",
                error,
            )

            video.status = "Failed"

            db.commit()