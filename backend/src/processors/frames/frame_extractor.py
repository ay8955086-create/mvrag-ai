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
    Extracts representative frames from a video
    at a configurable time interval.
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
        """
        Extract representative frames from a video.

        A frame is saved every `interval_seconds`.

        Example:
            25 FPS + 2 second interval
            ≈ 1 saved frame every 50 video frames.
        """

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

        if fps <= 0:
            fps = 30.0

        frame_count = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        duration = (
            frame_count / fps
            if frame_count > 0
            else 0
        )

        frame_interval = max(
            1,
            int(
                round(
                    fps * self.interval_seconds
                )
            ),
        )

        estimated_frames = (
            int(duration / self.interval_seconds) + 1
            if duration > 0
            else 0
        )

        logger.info(
            "============================================================"
        )

        logger.info(
            "Frame extraction started."
        )

        logger.info(
            "Video       : %s",
            video_path.name,
        )

        logger.info(
            "FPS         : %.2f",
            fps,
        )

        logger.info(
            "Total frames: %d",
            frame_count,
        )

        logger.info(
            "Duration    : %.2f seconds",
            duration,
        )

        logger.info(
            "Interval    : %.2f seconds",
            self.interval_seconds,
        )

        logger.info(
            "Expected sampled frames: approximately %d",
            estimated_frames,
        )

        logger.info(
            "============================================================"
        )

        extracted_frames: list[FrameInfo] = []

        frame_number = 0
        saved = 0

        while True:

            success, frame = capture.read()

            if not success:
                break

            if frame_number % frame_interval == 0:

                timestamp = (
                    frame_number / fps
                )

                filename = (
                    output_dir
                    / f"frame_{saved:05d}.jpg"
                )

                # Resize before saving.
                # This reduces the amount of data
                # sent to OCR and BLIP.
                frame = cv2.resize(
                    frame,
                    (960, 540),
                    interpolation=cv2.INTER_AREA,
                )

                written = cv2.imwrite(
                    str(filename),
                    frame,
                )

                if not written:
                    logger.warning(
                        "Failed to save frame: %s",
                        filename,
                    )

                else:

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

                    if saved % 10 == 0:

                        logger.info(
                            "Sampled %d frames | timestamp %.2f sec",
                            saved,
                            timestamp,
                        )

            frame_number += 1

        capture.release()

        logger.info(
            "============================================================"
        )

        logger.info(
            "Frame extraction completed."
        )

        logger.info(
            "Frames decoded : %d",
            frame_number,
        )

        logger.info(
            "Frames saved   : %d",
            len(extracted_frames),
        )

        logger.info(
            "Output folder  : %s",
            output_dir,
        )

        logger.info(
            "============================================================"
        )

        return extracted_frames