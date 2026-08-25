"""
Retrieval service for MVRAG AI.

Combines semantic retrieval and reranking.
"""

from __future__ import annotations

from src.core.logger import get_logger
from src.retrieval.reranker import Reranker
from src.retrieval.retriever import Retriever

logger = get_logger(__name__)


class RetrievalService:
    """High-level retrieval service."""

    def __init__(self):
        self.retriever = Retriever()
        self.reranker = Reranker()
        logger.info("RetrievalService initialized.")

    def retrieve_context(
        self,
        query: str,
        video_id: int | None = None,
    ) -> list[dict]:
        """Retrieve and rerank relevant multimodal chunks."""

        logger.info(
            "Starting retrieval service | video_id=%s",
            video_id,
        )

        retrieval_results = self.retriever.retrieve(
            query=query,
            video_id=video_id,
        )

        documents = (
            retrieval_results.get("documents") or [[]]
        )[0]

        metadata = (
            retrieval_results.get("metadatas") or [[]]
        )[0]

        distances = (
            retrieval_results.get("distances") or [[]]
        )[0]

        ids = (
            retrieval_results.get("ids") or [[]]
        )[0]

        ranked_results = self.reranker.rerank(
            query=query,
            documents=documents,
            metadata=metadata,
            distances=distances,
            ids=ids,
        )

        logger.info(
            "Retrieved %d final chunks.",
            len(ranked_results),
        )

        return ranked_results
