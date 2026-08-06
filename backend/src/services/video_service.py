"""
Video service for MVRAG AI.
"""

from __future__ import annotations

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.core.logger import get_logger
from src.models.video import Video
from src.pipeline.video_pipeline import VideoPipeline
from src.utils.video_metadata import extract_video_metadata

logger = get_logger(__name__)


class VideoService:
    """
    Handles all video upload operations.
    """

    ALLOWED_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
    }

    @staticmethod
    def upload_video(
        db: Session,
        file: UploadFile,
        title: str,
        description: str | None = None,
    ) -> Video:
        """
        Upload a video, process it through the AI pipeline,
        and store its metadata.
        """

        # ----------------------------------------------------------
        # Validate file extension
        # ----------------------------------------------------------

        extension = Path(file.filename).suffix.lower()

        if extension not in VideoService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported video format.",
            )

        # ----------------------------------------------------------
        # Save uploaded file
        # ----------------------------------------------------------

        unique_filename = f"{uuid.uuid4()}{extension}"

        save_path = settings.raw_video_dir / unique_filename

        logger.info(
            "Saving uploaded video to %s",
            save_path,
        )

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # ----------------------------------------------------------
        # Extract metadata
        # ----------------------------------------------------------

        metadata = extract_video_metadata(
            str(save_path),
        )

        # ----------------------------------------------------------
        # Create database record
        # ----------------------------------------------------------

        video = Video(
            filename=unique_filename,
            title=title,
            description=description,

            duration=metadata["duration"],
            fps=metadata["fps"],
            width=metadata["width"],
            height=metadata["height"],
            size_mb=metadata["size_mb"],

            status="Processing",
            upload_time=datetime.now(UTC),
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        logger.info(
            "Video record created with ID %d",
            video.id,
        )

        # ----------------------------------------------------------
        # Run AI Pipeline
        # ----------------------------------------------------------

        pipeline = VideoPipeline()

        try:

            logger.info(
                "Starting AI pipeline..."
            )

            pipeline_result = pipeline.process(
                save_path,
            )

            # Reserved for future use:
            # transcript
            # OCR
            # captions
            # chunks
            # embeddings

            _ = pipeline_result

            video.status = "Completed"

            logger.info(
                "AI pipeline completed successfully."
            )

        except Exception:

            logger.exception(
                "Pipeline processing failed."
            )

            video.status = "Failed"

            db.commit()

            raise

        # ----------------------------------------------------------
        # Update status
        # ----------------------------------------------------------

        db.commit()
        db.refresh(video)

        logger.info(
            "Video processing finished."
        )

        return video
    
    @staticmethod
    def get_all_videos(
        db: Session,
    ) -> list[Video]:
        """
        Return all uploaded videos.
        """

        logger.info("Fetching all videos.")

        return (
            db.query(Video)
            .order_by(Video.upload_time.desc())
            .all()
        )

    @staticmethod
    def get_video(
        db: Session,
        video_id: int,
    ) -> Video:
        """
        Return one video.
        """

        video = db.get(
            Video,
            video_id,
        )

        if video is None:

            raise HTTPException(
                status_code=404,
                detail="Video not found.",
            )

        return video

    @staticmethod
    def delete_video(
        db: Session,
        video_id: int,
    ) -> dict:
        """
        Delete a video.
        """

        video = db.get(
            Video,
            video_id,
        )

        if video is None:

            raise HTTPException(
                status_code=404,
                detail="Video not found.",
            )

        video_path = (
            settings.raw_video_dir
            / video.filename
        )

        if video_path.exists():
            video_path.unlink()

        db.delete(video)
        db.commit()

        logger.info(
            "Video %d deleted.",
            video_id,
        )

        return {
            "message": "Video deleted successfully."
        }