"""
Efficient frame extraction module for MVRAG AI.

Extracts representative frames by seeking directly to timestamps
instead of decoding every frame in the video.
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
    Extract representative frames efficiently.

    Instead of reading every frame, this implementation seeks
    directly to the required timestamps.
    """

    def __init__(
        self,
        interval_seconds: float | None = None,
    ):
        self.interval_seconds = (
            float(interval_seconds)
            if interval_seconds is not None
            else float(settings.FRAME_INTERVAL_SECONDS)
        )

        if self.interval_seconds <= 0:
            raise ValueError(
                "FRAME_INTERVAL_SECONDS must be greater than 0."
            )

    def extract(
        self,
        video_path: str | Path,
    ) -> list[FrameInfo]:

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        output_dir = (
            settings.frames_dir
            / video_path.stem
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        capture = cv2.VideoCapture(
            str(video_path)
        )

        if not capture.isOpened():
            raise RuntimeError(
                f"Unable to open video: {video_path}"
            )

        fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        frame_count = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        if fps <= 0:
            fps = 30.0

        duration = (
            frame_count / fps
            if frame_count > 0
            else 0.0
        )

        logger.info(
            "Frame extraction started."
        )

        logger.info(
            "Video: %s",
            video_path.name,
        )

        logger.info(
            "FPS: %.2f",
            fps,
        )

        logger.info(
            "Duration: %.2f seconds",
            duration,
        )

        logger.info(
            "Frame interval: %.2f seconds",
            self.interval_seconds,
        )

        estimated_count = (
            int(duration / self.interval_seconds) + 1
        )

        logger.info(
            "Expected frames: approximately %d",
            estimated_count,
        )

        extracted_frames: list[FrameInfo] = []

        timestamp = 0.0
        saved = 0

        while timestamp <= duration:

            # Seek directly to the requested timestamp.
            capture.set(
                cv2.CAP_PROP_POS_MSEC,
                timestamp * 1000.0,
            )

            success, frame = capture.read()

            if not success:

                logger.warning(
                    "Could not read frame at %.2f seconds.",
                    timestamp,
                )

                timestamp += self.interval_seconds

                continue

            frame = cv2.resize(
                frame,
                (960, 540),
                interpolation=cv2.INTER_AREA,
            )

            filename = (
                output_dir
                / f"frame_{saved:05d}.jpg"
            )

            if not cv2.imwrite(
                str(filename),
                frame,
            ):

                logger.warning(
                    "Failed to save frame: %s",
                    filename,
                )

                timestamp += self.interval_seconds

                continue

            extracted_frames.append(
                FrameInfo(
                    frame=filename,
                    timestamp=round(
                        timestamp,
                        2,
                    ),
                )
            )

            saved += 1

            logger.info(
                "Saved frame %d at %.2f seconds.",
                saved,
                timestamp,
            )

            timestamp += self.interval_seconds

        capture.release()

        logger.info(
            "Frame extraction completed."
        )

        logger.info(
            "Frames saved: %d",
            len(extracted_frames),
        )

        return extracted_frames