from __future__ import annotations

import shutil
import uuid
from datetime import datetime, UTC
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.models.video import Video
from src.utils.video_metadata import extract_video_metadata


class VideoService:
    """
    Handles all video upload operations.
    """

    ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

    @staticmethod
    def upload_video(
        db: Session,
        file: UploadFile,
        title: str,
        description: str | None = None,
    ) -> Video:
        """
        Save a video, extract metadata, and create a database record.
        """

        extension = Path(file.filename).suffix.lower()

        if extension not in VideoService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported video format.",
            )

        unique_filename = f"{uuid.uuid4()}{extension}"

        save_path = settings.raw_video_dir / unique_filename

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        metadata = extract_video_metadata(str(save_path))

        video = Video(
            filename=unique_filename,
            title=title,
            description=description,

            duration=metadata["duration"],
            fps=metadata["fps"],
            width=metadata["width"],
            height=metadata["height"],
            size_mb=metadata["size_mb"],

            status="Pending",
            upload_time=datetime.now(UTC),
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        return video