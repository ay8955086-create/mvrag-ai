"""
Video service for MVRAG AI.
"""

from __future__ import annotations

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import BackgroundTasks, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.core.logger import get_logger
from src.models.video import Video
from src.services.background_service import BackgroundService
from src.utils.video_metadata import extract_video_metadata

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
        Upload a video and schedule AI processing
        in the background.

        The HTTP request returns immediately after the
        video record is created.
        """

        # ------------------------------------------------------
        # Validate filename
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Generate unique filename
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Save uploaded file
        # ------------------------------------------------------

        try:

            with save_path.open("wb") as buffer:

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

        # ------------------------------------------------------
        # Extract metadata
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Create database record
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Schedule background AI processing
        # ------------------------------------------------------

        if background_tasks is None:

            logger.warning(
                "BackgroundTasks was not provided. "
                "Video %d will remain in Processing state.",
                video.id,
            )

        else:

            background_tasks.add_task(
                BackgroundService.process_video,
                video.id,
            )

            logger.info(
                "Background AI processing scheduled "
                "for video %d.",
                video.id,
            )

        # ------------------------------------------------------
        # IMPORTANT:
        # Return immediately.
        #
        # DO NOT run VideoPipeline here.
        # ------------------------------------------------------

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