"""
Whisper transcription module for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

import whisper

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class WhisperTranscriber:
    """
    Transcribes audio using OpenAI Whisper.
    """

    def __init__(self):
        logger.info("Loading Whisper model: %s", settings.WHISPER_MODEL)
        self.model = whisper.load_model(settings.WHISPER_MODEL)

    def transcribe(self, audio_path: str | Path):
        """
        Transcribe an audio file.

        Parameters
        ----------
        audio_path : str | Path

        Returns
        -------
        dict
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        logger.info("Transcribing %s", audio_path.name)

        result = self.model.transcribe(
    str(audio_path),
    fp16=False,
    verbose=False,
)

        logger.info("Transcription completed.")

        return result