from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FrameInfo:
    """
    Represents one extracted frame.
    """

    frame: Path

    timestamp: float