"""
Media streaming endpoints for uploaded videos.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.config.settings import settings

router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@router.get(
    "/videos/{filename}",
    response_class=FileResponse,
)
def get_video_media(filename: str):
    """
    Serve an uploaded video to the browser.

    Only the filename component is accepted; directory traversal
    is prevented by resolving Path(filename).name.
    """

    safe_filename = Path(filename).name

    if not safe_filename:
        raise HTTPException(
            status_code=404,
            detail="Video file not found.",
        )

    video_path = (
        settings.raw_video_dir
        / safe_filename
    )

    if not video_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Video file not found.",
        )

    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=safe_filename,
    )
