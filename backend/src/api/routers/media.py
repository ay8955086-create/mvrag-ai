"""
Media streaming endpoints for uploaded videos.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from src.config.settings import settings


router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@router.get("/videos/{filename}")
async def get_video_media(
    filename: str,
    request: Request,
):
    """
    Stream uploaded video files with proper HTTP Range support.

    Browsers use Range requests for video playback and seeking.
    """

    # ----------------------------------------------------------
    # Secure filename
    # ----------------------------------------------------------

    safe_filename = Path(filename).name

    if not safe_filename:
        raise HTTPException(
            status_code=404,
            detail="Video file not found.",
        )

    # ----------------------------------------------------------
    # Locate video
    # ----------------------------------------------------------

    video_path = (
        settings.raw_video_dir
        / safe_filename
    )

    if not video_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Video file not found.",
        )

    # ----------------------------------------------------------
    # File information
    # ----------------------------------------------------------

    file_size = video_path.stat().st_size

    media_type, _ = mimetypes.guess_type(
        str(video_path)
    )

    if media_type is None:
        media_type = "video/mp4"

    # ----------------------------------------------------------
    # Read Range header
    # ----------------------------------------------------------

    range_header = request.headers.get("range")

    # ----------------------------------------------------------
    # No Range header
    # ----------------------------------------------------------

    if not range_header:
        content = video_path.read_bytes()

        return Response(
            content=content,
            status_code=200,
            media_type=media_type,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
                "Content-Disposition": (
                    f'inline; filename="{safe_filename}"'
                ),
            },
        )

    # ----------------------------------------------------------
    # Parse Range header
    # ----------------------------------------------------------

    try:
        range_value = range_header.strip().lower()

        if not range_value.startswith("bytes="):
            raise ValueError("Invalid range unit.")

        range_spec = range_value.replace(
            "bytes=",
            "",
            1,
        ).split(",")[0].strip()

        start_str, end_str = range_spec.split(
            "-",
            1,
        )

        # ------------------------------------------------------
        # Range: bytes=500-
        # ------------------------------------------------------

        if start_str:
            start = int(start_str)

            if start >= file_size:
                raise ValueError(
                    "Range start is outside the file."
                )

        # ------------------------------------------------------
        # Range: bytes=-500
        # ------------------------------------------------------

        else:
            suffix_length = int(end_str)

            if suffix_length <= 0:
                raise ValueError(
                    "Invalid suffix range."
                )

            suffix_length = min(
                suffix_length,
                file_size,
            )

            start = file_size - suffix_length

        # ------------------------------------------------------
        # Determine end
        # ------------------------------------------------------

        if end_str:
            end = min(
                int(end_str),
                file_size - 1,
            )
        else:
            # Limit each streaming response to 1 MB.
            end = min(
                start + 1024 * 1024 - 1,
                file_size - 1,
            )

        if start > end:
            raise ValueError(
                "Invalid byte range."
            )

    except (ValueError, TypeError):
        return Response(
            status_code=416,
            headers={
                "Content-Range": f"bytes */{file_size}",
                "Accept-Ranges": "bytes",
            },
        )

    # ----------------------------------------------------------
    # Read ONLY requested bytes
    # ----------------------------------------------------------

    content_length = end - start + 1

    with video_path.open("rb") as video_file:
        video_file.seek(start)
        content = video_file.read(content_length)

    # ----------------------------------------------------------
    # Return proper 206 response
    # ----------------------------------------------------------

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Range": (
            f"bytes {start}-{end}/{file_size}"
        ),
        "Content-Length": str(len(content)),
        "Content-Disposition": (
            f'inline; filename="{safe_filename}"'
        ),
        "Cache-Control": "public, max-age=3600",
    }

    return Response(
        content=content,
        status_code=206,
        media_type=media_type,
        headers=headers,
    )