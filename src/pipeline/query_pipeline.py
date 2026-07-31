"""
Query pipeline for MVRAG AI.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.retrieval.retrieval_service import RetrievalService

logger = get_logger(__name__)


class QueryPipeline:
    """
    Executes the query pipeline.
    """

    def __init__(self):

        self.retrieval_service = RetrievalService()

        logger.info("QueryPipeline initialized.")

    def process_query(
        self,
        question: str,
    ) -> dict:
        """
        Process a user question.
        """

        logger.info(
            "Processing question: %s",
            question,
        )

        context = self.retrieval_service.retrieve_context(
            question,
        )

        return {
            "question": question,
            "context": context,
        }