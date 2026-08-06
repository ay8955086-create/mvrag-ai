"""
Audio utility functions.
"""

from pathlib import Path


def audio_exists(audio_path: str | Path) -> bool:
    return Path(audio_path).exists()