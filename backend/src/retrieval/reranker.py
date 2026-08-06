"""
Reranker module for MVRAG AI.

Uses BAAI BGE-Reranker to improve retrieval quality.
"""

from __future__ import annotations

from sentence_transformers import CrossEncoder

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class Reranker:
    """
    Reranks retrieved chunks using BGE-Reranker.
    """

    def __init__(self):

        logger.info(
            "Loading reranker model: %s",
            settings.RERANKER_MODEL,
        )

        self.model = CrossEncoder(
            settings.RERANKER_MODEL,
        )

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int = 3,
    ) -> list[dict]:

        if not documents:
            return []

        pairs = [
            [query, document]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            {
                "document": document,
                "score": float(score),
            }
            for document, score in ranked[:top_k]
        ]