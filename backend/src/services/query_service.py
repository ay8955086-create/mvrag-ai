"""
Query service for MVRAG AI.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.pipeline.query_pipeline import QueryPipeline

logger = get_logger(__name__)


class QueryService:
    """Handles user queries."""

    def __init__(self):
        self.pipeline = QueryPipeline()

    def ask(
        self,
        question: str,
        video_id: int | None = None,
    ) -> dict:
        logger.info(
            "Received question: %s | video_id=%s",
            question,
            video_id,
        )

        return self.pipeline.process_query(
            question=question,
            video_id=video_id,
        )
