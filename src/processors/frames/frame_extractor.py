"""
Frame extraction module for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

import cv2

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class FrameExtractor:
    """
    Extracts frames from a video at a fixed interval.
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
    ) -> list[Path]:

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(video_path)

        output_dir = settings.frames_dir / video_path.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        capture = cv2.VideoCapture(str(video_path))

        if not capture.isOpened():
            raise RuntimeError("Unable to open video.")

        fps = capture.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30

        frame_interval = int(fps * self.interval_seconds)

        saved_frames = []

        frame_number = 0
        saved = 0

        logger.info("Extracting frames from %s", video_path.name)

        while True:

            success, frame = capture.read()

            if not success:
                break

            if frame_number % frame_interval == 0:

                filename = output_dir / f"frame_{saved:05d}.jpg"

                frame = cv2.resize(frame, (960, 540))

                cv2.imwrite(str(filename), frame)

                saved_frames.append(filename)

                saved += 1

            frame_number += 1

        capture.release()

        logger.info("Extracted %d frames.", len(saved_frames))

        return saved_frames