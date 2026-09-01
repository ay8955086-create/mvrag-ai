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

        The video has already been normalized by
        VideoService before this task starts.
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

            # ==================================================
            # Load video
            # ==================================================

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

            # ==================================================
            # Locate normalized video
            # ==================================================

            video_path = (
                settings.raw_video_dir
                / video.filename
            )

            if not video_path.is_file():

                raise FileNotFoundError(
                    f"Video file not found: {video_path}"
                )

            logger.info(
                "Video path: %s",
                video_path,
            )

            # ==================================================
            # Run complete AI pipeline
            # ==================================================

            pipeline = VideoPipeline(
                db=db,
                video_id=video_id,
            )

            # --------------------------------------------------
            # Remove old vectors for this video
            # --------------------------------------------------

            pipeline.chroma_store.delete_by_video_id(
                video_id
            )

            # --------------------------------------------------
            # Process normalized video
            # --------------------------------------------------

            pipeline.process(
                video_path
            )

            # ==================================================
            # Processing completed
            # ==================================================

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
                "Background processing failed "
                "for video %d: %s",
                video_id,
                error,
            )

            # ==================================================
            # Mark video as failed
            # ==================================================

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
                    "Failed to update video %d "
                    "status to Failed.",
                    video_id,
                )

        finally:

            db.close()

            logger.info(
                "Background database session closed "
                "for video %d.",
                video_id,
            )