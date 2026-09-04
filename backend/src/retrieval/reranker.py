"""
Reranker module for MVRAG AI.

Uses BAAI BGE-Reranker to improve retrieval quality.
"""

from __future__ import annotations

import math



from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

class Reranker:
    """Reranks retrieved multimodal chunks."""

    def __init__(self):
        from sentence_transformers import CrossEncoder

        logger.info(
            "Loading reranker model: %s",
            settings.RERANKER_MODEL,
        )
        self.model = CrossEncoder(settings.RERANKER_MODEL)

    def rerank(
        self,
        query: str,
        documents: list[str],
        metadata: list[dict] | None = None,
        distances: list[float] | None = None,
        ids: list[str] | None = None,
        top_k: int = 3,
    ) -> list[dict]:
        if not documents:
            return []

        metadata = metadata or [{} for _ in documents]
        distances = distances or [None for _ in documents]
        ids = ids or [None for _ in documents]

        pairs = [[query, document] for document in documents]
        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(
                documents,
                scores,
                metadata,
                distances,
                ids,
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        results = []

        for document, score, item_metadata, distance, embedding_id in ranked[:top_k]:
            logit = float(score)
            relevance = 1.0 / (1.0 + math.exp(-max(-60.0, min(60.0, logit))))

            item = {
                "document": document,
                "score": relevance,
            }

            if distance is not None:
                item["distance"] = float(distance)

            if embedding_id is not None:
                item["embedding_id"] = embedding_id

            item.update(item_metadata or {})
            results.append(item)

        return results