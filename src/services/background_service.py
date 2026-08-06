"""
Background processing service for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from src.core.logger import get_logger
from src.models.processing_status import ProcessingStatus
from src.models.video import Video
from src.pipeline.video_pipeline import VideoPipeline
from src.config.settings import settings

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
            logger.error("Video not found.")
            return

        processing = (
            db.query(ProcessingStatus)
            .filter(
                ProcessingStatus.video_id == video_id
            )
            .first()
        )

        if processing is None:

            processing = ProcessingStatus(
                video_id=video_id,
                status="Processing",
                current_step="Initializing",
                progress=0,
            )

            db.add(processing)
            db.commit()

        try:

            pipeline = VideoPipeline(
                db=db,
                video_id=video_id,
            )

            video_path = settings.raw_video_dir / video.filename

            pipeline.process(
            video_path,
)

            video.status = "Completed"

            db.commit()

            logger.info(
                "Background processing completed."
            )

        except Exception as error:

            logger.exception(error)

            video.status = "Failed"

            processing.status = "Failed"

            processing.current_step = str(error)

            db.commit()