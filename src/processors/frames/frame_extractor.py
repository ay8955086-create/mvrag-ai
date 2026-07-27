"""
Frame extraction module for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

import cv2

from src.config.settings import settings
from src.core.logger import get_logger
from src.models.frame_info import FrameInfo

logger = get_logger(__name__)


class FrameExtractor:
    """
    Extracts frames from a video at a configurable interval.
    """

    def __init__(
        self,
        interval_seconds: int | None = None,
    ):
        self.interval_seconds = (
            interval_seconds
            if interval_seconds is not None
            else settings.FRAME_INTERVAL_SECONDS
        )

    def extract(
        self,
        video_path: str | Path,
    ) -> list[FrameInfo]:
        """
        Extract frames from a video.

        Parameters
        ----------
        video_path : str | Path
            Path to the input video.

        Returns
        -------
        list[FrameInfo]
            Extracted frame information including timestamps.
        """

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(video_path)

        output_dir = settings.frames_dir / video_path.stem
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        capture = cv2.VideoCapture(str(video_path))

        if not capture.isOpened():
            raise RuntimeError(
                f"Unable to open video: {video_path}"
            )

        fps = capture.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30

        frame_interval = int(fps * self.interval_seconds)

        extracted_frames: list[FrameInfo] = []

        frame_number = 0
        saved = 0

        logger.info(
            "Extracting frames from %s",
            video_path.name,
        )

        while True:

            success, frame = capture.read()

            if not success:
                break

            if frame_number % frame_interval == 0:

                timestamp = frame_number / fps

                filename = (
                    output_dir
                    / f"frame_{saved:05d}.jpg"
                )

                # Resize for faster OCR & BLIP
                frame = cv2.resize(
                    frame,
                    (960, 540),
                )

                cv2.imwrite(
                    str(filename),
                    frame,
                )

                extracted_frames.append(
                    FrameInfo(
                        frame=filename,
                        timestamp=round(timestamp, 2),
                    )
                )

                saved += 1

            frame_number += 1

        capture.release()

        logger.info(
            "Extracted %d frames.",
            len(extracted_frames),
        )

        return extracted_frames