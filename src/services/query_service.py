"""
Query service for MVRAG AI.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.pipeline.query_pipeline import QueryPipeline

logger = get_logger(__name__)


class QueryService:
    """
    Handles user queries.
    """

    def __init__(self):

        self.pipeline = QueryPipeline()

    def ask(
        self,
        question: str,
    ) -> dict:
        """
        Process a user question.
        """

        logger.info(
            "Received question: %s",
            question,
        )

        return self.pipeline.process_query(
            question,
        )