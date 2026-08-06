"""
Retrieval service for MVRAG AI.

Combines semantic retrieval and reranking.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker

logger = get_logger(__name__)


class RetrievalService:
    """
    High-level retrieval service.
    """

    def __init__(self):

        self.retriever = Retriever()
        self.reranker = Reranker()

        logger.info("RetrievalService initialized.")

    def retrieve_context(
        self,
        query: str,
    ) -> list[dict]:
        """
        Retrieve and rerank the most relevant chunks.
        """

        logger.info("Starting retrieval service.")

        retrieval_results = self.retriever.retrieve(query)

        documents = retrieval_results["documents"][0]

        ranked_results = self.reranker.rerank(
            query=query,
            documents=documents,
        )

        logger.info(
            "Retrieved %d final chunks.",
            len(ranked_results),
        )

        return ranked_results