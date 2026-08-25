"""
Background processing service for MVRAG AI.
"""

from __future__ import annotations

from datetime import UTC, datetime

from src.config.settings import settings
from src.core.logger import get_logger
from src.database.session import SessionLocal
from src.models.video import Video
from src.pipeline.video_pipeline import VideoPipeline

logger = get_logger(__name__)


class BackgroundService:
    """
    Executes long-running video processing tasks
    outside the upload HTTP request.
    """

    @staticmethod
    def process_video(
        video_id: int,
    ) -> None:
        """
        Process a video in the background.

        A new database session is created here because the
        original FastAPI request session may already be closed.
        """

        db = SessionLocal()

        try:

            logger.info(
                "=" * 60
            )

            logger.info(
                "Background processing started for video %d",
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

            video.status = "Processing"

            db.commit()

            video_path = (
                settings.raw_video_dir
                / video.filename
            )

            if not video_path.exists():

                raise FileNotFoundError(
                    f"Video file not found: {video_path}"
                )

            logger.info(
                "Video path: %s",
                video_path,
            )

            # --------------------------------------------------
            # Run complete AI pipeline
            # --------------------------------------------------

            pipeline = VideoPipeline(
                db=db,
                video_id=video_id,
            )

            # Remove vectors from an earlier processing run for this
            # video before rebuilding its index.
            pipeline.chroma_store.delete_by_video_id(
                video_id
            )

            pipeline.process(
                video_path
            )

            # --------------------------------------------------
            # Processing completed
            # --------------------------------------------------

            video.status = "Completed"

            video.processed_time = datetime.now(
                UTC
            )

            db.commit()

            logger.info(
                "Video %d processing completed successfully.",
                video_id,
            )

            logger.info(
                "=" * 60
            )

        except Exception as error:

            logger.exception(
                "Background processing failed for video %d: %s",
                video_id,
                error,
            )

            try:

                video = db.get(
                    Video,
                    video_id,
                )

                if video is not None:

                    video.status = "Failed"

                    db.commit()

            except Exception:

                logger.exception(
                    "Failed to update video %d status to Failed.",
                    video_id,
                )

        finally:

            db.close()

            logger.info(
                "Background database session closed for video %d.",
                video_id,
            )