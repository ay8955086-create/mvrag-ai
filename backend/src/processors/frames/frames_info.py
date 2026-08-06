from dataclasses import dataclass
from pathlib import Path


@dataclass
class FrameInfo:
    frame_number: int
    timestamp: float
    image_path: Path