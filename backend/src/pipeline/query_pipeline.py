"""
Query pipeline for MVRAG AI.

Processes user questions by retrieving relevant context
and generating answers using the configured LLM.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.llm.llm_service import LLMService
from src.retrieval.retrieval_service import RetrievalService

logger = get_logger(__name__)


class QueryPipeline:
    """Executes the complete query pipeline."""

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        logger.info("QueryPipeline initialized.")

    def process_query(
        self,
        question: str,
        video_id: int | None = None,
    ) -> dict:
        logger.info("=" * 60)
        logger.info(
            "Processing Question | video_id=%s",
            video_id,
        )
        logger.info("Question: %s", question)

        context = self.retrieval_service.retrieve_context(
            query=question,
            video_id=video_id,
        )

        logger.info(
            "Retrieved %d context chunks.",
            len(context),
        )

        answer = self.llm_service.answer(
            question,
            context,
        )

        logger.info("Answer generated successfully.")
        logger.info("=" * 60)

        return {
            "question": question,
            "video_id": video_id,
            "context": context,
            "answer": answer,
        }
