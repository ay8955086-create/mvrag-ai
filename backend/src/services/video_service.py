"""
Video service for MVRAG AI.
"""

from __future__ import annotations

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import (
    BackgroundTasks,
    HTTPException,
    UploadFile,
)
from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from src.config.settings import settings
from src.core.logger import get_logger
from src.models.analytics import Analytics
from src.models.video import Video
from src.processors.video_normalizer import (
    VideoNormalizer,
)
from src.utils.video_metadata import (
    extract_video_metadata,
)


logger = get_logger(__name__)


class VideoService:
    """
    Handles video upload and video management operations.
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
        background_tasks: BackgroundTasks | None = None,
    ) -> Video:
        """
        Upload a video, normalize it for browser playback,
        create its database record, and schedule AI processing.

        The normalized video replaces the original uploaded
        file so the database filename always points to the
        browser-compatible file.
        """

        # ======================================================
        # Validate filename
        # ======================================================

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="Video filename is required.",
            )

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        if extension not in VideoService.ALLOWED_EXTENSIONS:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported video format. "
                    "Allowed formats: MP4, AVI, MOV, MKV."
                ),
            )

        # ======================================================
        # Generate unique filename
        # ======================================================

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        save_path = (
            settings.raw_video_dir
            / unique_filename
        )

        logger.info(
            "Saving uploaded video to %s",
            save_path,
        )

        # ======================================================
        # Save uploaded file
        # ======================================================

        try:

            with save_path.open(
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

        except Exception:

            logger.exception(
                "Failed to save uploaded video."
            )

            if save_path.exists():
                save_path.unlink()

            raise HTTPException(
                status_code=500,
                detail="Failed to save uploaded video.",
            )

        # ======================================================
        # Normalize video
        # ======================================================

        normalized_path = None

        try:

            logger.info(
                "Normalizing uploaded video for "
                "browser playback."
            )

            normalizer = VideoNormalizer()

            normalized_path = normalizer.normalize(
                save_path
            )

            # --------------------------------------------------
            # Replace the original file with the normalized file
            # --------------------------------------------------

            save_path.unlink()

            normalized_path.rename(
                save_path
            )

            logger.info(
                "Browser-compatible video created: %s",
                save_path,
            )

        except Exception:

            logger.exception(
                "Failed to normalize uploaded video."
            )

            if normalized_path is not None:

                if normalized_path.exists():
                    normalized_path.unlink()

            if save_path.exists():
                save_path.unlink()

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unable to prepare the uploaded video "
                    "for browser playback."
                ),
            )

        # ======================================================
        # Extract metadata AFTER normalization
        # ======================================================

        try:

            metadata = extract_video_metadata(
                str(save_path)
            )

        except Exception:

            logger.exception(
                "Failed to extract video metadata."
            )

            if save_path.exists():
                save_path.unlink()

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unable to read the uploaded video. "
                    "Please verify that the file is valid."
                ),
            )

        # ======================================================
        # Create database record
        # ======================================================

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

        # ======================================================
        # Schedule background AI processing
        # ======================================================

        if background_tasks is None:

            logger.warning(
                "BackgroundTasks was not provided. "
                "Video %d will remain in Processing state.",
                video.id,
            )

        else:

    from src.services.background_service import BackgroundService

    background_tasks.add_task(
        BackgroundService.process_video,
        video.id,
    )
            logger.info(
                "Background AI processing scheduled "
                "for video %d.",
                video.id,
            )

        # ======================================================
        # Return immediately
        # ======================================================

        return video

    # ==========================================================
    # Get All Videos
    # ==========================================================

    @staticmethod
    def get_all_videos(
        db: Session,
    ) -> list[Video]:
        """
        Return all uploaded videos.
        """

        logger.info(
            "Fetching all videos."
        )

        return (
            db.query(Video)
            .order_by(
                Video.upload_time.desc()
            )
            .all()
        )

    # ==========================================================
    # Get Single Video
    # ==========================================================

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

    # ==========================================================
    # Get Extended Video Details
    # ==========================================================

    @staticmethod
    def get_extended_video(
        db: Session,
        video_id: int,
    ) -> Video:
        """
        Return a video together with its persisted
        multimodal results.
        """

        statement = (
            select(Video)
            .options(
                selectinload(
                    Video.transcripts
                ),
                selectinload(
                    Video.ocr_results
                ),
                selectinload(
                    Video.captions
                ),
                selectinload(
                    Video.chunks
                ),
                selectinload(
                    Video.analytics
                ),
            )
            .where(
                Video.id == video_id
            )
        )

        video = (
            db.execute(statement)
            .scalar_one_or_none()
        )

        if video is None:

            raise HTTPException(
                status_code=404,
                detail="Video not found.",
            )

        return video

    # ==========================================================
    # Delete Video
    # ==========================================================

    @staticmethod
    def delete_video(
        db: Session,
        video_id: int,
    ) -> dict:
        """
        Delete a video and its raw file.
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