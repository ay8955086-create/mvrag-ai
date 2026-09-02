"""
SQLAlchemy ORM models for MVRAG AI.

Importing this package registers every ORM model with SQLAlchemy's
metadata so Base.metadata.create_all() can create all tables.
"""

from .analytics import Analytics
from .caption import Caption
from .chunk import Chunk
from .ocr import OCRResult
from .query import Query
from .transcript import Transcript
from .video import Video

__all__ = [
    "Video",
    "Transcript",
    "OCRResult",
    "Caption",
    "Chunk",
    "Query",
    "Analytics",
]