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
    """
    Executes the complete query pipeline.

    Workflow:
        Question
            ↓
        Retriever
            ↓
        Reranker
            ↓
        LLM
            ↓
        Final Answer
    """

    def __init__(self):
        """
        Initialize all query components.
        """

        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

        logger.info("QueryPipeline initialized.")

    # ==========================================================
    # Query Pipeline
    # ==========================================================

    def process_query(
        self,
        question: str,
    ) -> dict:
        """
        Process a user question.
        """

        logger.info("=" * 60)
        logger.info("Processing Question")
        logger.info("Question: %s", question)

        # ------------------------------------------------------
        # Step 1 : Retrieve Context
        # ------------------------------------------------------

        context = self.retrieval_service.retrieve_context(
            question,
        )

        logger.info(
            "Retrieved %d context chunks.",
            len(context),
        )

        # ------------------------------------------------------
        # Step 2 : Generate Answer
        # ------------------------------------------------------

        answer = self.llm_service.answer(
            question,
            context,
        )

        logger.info("Answer generated successfully.")
        logger.info("=" * 60)

        return {
            "question": question,
            "context": context,
            "answer": answer,
        }