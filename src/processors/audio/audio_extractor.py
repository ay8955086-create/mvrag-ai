"""
Audio extraction utilities for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

import ffmpeg

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class AudioExtractor:
    """
    Extract audio from video files using FFmpeg.
    """

    @staticmethod
    def extract(video_path: str | Path) -> Path:
        """
        Extract audio from a video.

        Parameters
        ----------
        video_path : str | Path

        Returns
        -------
        Path
            Extracted audio (.wav) file path.
        """

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(video_path)

        settings.audio_dir.mkdir(parents=True, exist_ok=True)

        output_path = settings.audio_dir / f"{video_path.stem}.wav"

        logger.info("Extracting audio from %s", video_path.name)

        (
            ffmpeg
            .input(str(video_path))
            .output(
                str(output_path),
                ac=1,
                ar=16000,
            )
            .overwrite_output()
            .run(quiet=True)
        )

        logger.info("Audio saved to %s", output_path)

        return output_path