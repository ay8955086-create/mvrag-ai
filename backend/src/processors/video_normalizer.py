"""
Video normalization for MVRAG AI.

Uploaded videos are normalized to a browser-friendly MP4 container.

H.264/AAC streams are copied without re-encoding.
Incompatible codecs are converted to H.264/AAC.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from src.core.logger import get_logger


logger = get_logger(__name__)


class VideoNormalizer:
    """
    Normalize uploaded videos for reliable browser playback.
    """

    def _probe(
        self,
        input_path: Path,
    ) -> dict:
        """
        Inspect the input video using FFprobe.
        """

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-of",
            "json",
            str(input_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return json.loads(
            result.stdout or "{}"
        )

    def normalize(
        self,
        input_path: str | Path,
    ) -> Path:
        """
        Create a browser-compatible MP4.

        H.264 + AAC:
            Remux without re-encoding.

        Other codecs:
            Convert to H.264 + AAC.
        """

        input_path = Path(input_path)

        if not input_path.is_file():
            raise FileNotFoundError(
                input_path
            )

        output_path = (
            input_path.parent
            / f"{input_path.stem}_normalized.mp4"
        )

        if output_path.exists():
            output_path.unlink()

        # ------------------------------------------------------
        # Inspect streams
        # ------------------------------------------------------

        probe_data = self._probe(
            input_path
        )

        streams = probe_data.get(
            "streams",
            [],
        )

        video_stream = next(
            (
                stream
                for stream in streams
                if stream.get("codec_type") == "video"
            ),
            None,
        )

        audio_stream = next(
            (
                stream
                for stream in streams
                if stream.get("codec_type") == "audio"
            ),
            None,
        )

        if video_stream is None:
            raise RuntimeError(
                "Uploaded file does not contain a video stream."
            )

        video_codec = str(
            video_stream.get(
                "codec_name",
                "",
            )
        ).lower()

        audio_codec = (
            str(
                audio_stream.get(
                    "codec_name",
                    "",
                )
            ).lower()
            if audio_stream
            else None
        )

        logger.info(
            "Video normalization: "
            "video_codec=%s, audio_codec=%s",
            video_codec,
            audio_codec or "none",
        )

        # ------------------------------------------------------
        # H.264 + AAC
        #
        # No re-encoding required.
        #
        # This removes unwanted data streams such as
        # timed_id3 and adds faststart.
        # ------------------------------------------------------

        if video_codec == "h264" and (
            audio_codec is None
            or audio_codec == "aac"
        ):

            command = [
                "ffmpeg",
                "-y",
                "-i",
                str(input_path),

                "-map",
                "0:v:0",

                "-map",
                "0:a:0?",

                "-c:v",
                "copy",

                "-c:a",
                "copy",

                "-movflags",
                "+faststart",

                str(output_path),
            ]

        # ------------------------------------------------------
        # Incompatible codec
        #
        # Convert to H.264 + AAC.
        # ------------------------------------------------------

        else:

            logger.info(
                "Video requires codec conversion: "
                "video=%s audio=%s",
                video_codec,
                audio_codec or "none",
            )

            command = [
                "ffmpeg",
                "-y",
                "-i",
                str(input_path),

                "-map",
                "0:v:0",

                "-map",
                "0:a:0?",

                "-c:v",
                "libx264",

                "-preset",
                "veryfast",

                "-crf",
                "23",

                "-pix_fmt",
                "yuv420p",

                "-c:a",
                "aac",

                "-b:a",
                "128k",

                "-movflags",
                "+faststart",

                str(output_path),
            ]

        # ------------------------------------------------------
        # Execute FFmpeg
        # ------------------------------------------------------

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            logger.error(
                "FFmpeg normalization failed:\n%s",
                result.stderr,
            )

            raise RuntimeError(
                "Video normalization failed."
            )

        if not output_path.is_file():
            raise RuntimeError(
                "FFmpeg completed without creating "
                "the normalized video."
            )

        logger.info(
            "Video normalization completed: %s",
            output_path,
        )

        return output_path