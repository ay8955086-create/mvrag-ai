"""
BGE Reranker for MVRAG AI.
"""

from __future__ import annotations

from FlagEmbedding import FlagReranker

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class BGEReranker:

    def __init__(self):

        logger.info(
            "Loading reranker: %s",
            settings.RERANKER_MODEL,
        )

        self.model = FlagReranker(
            settings.RERANKER_MODEL,
            use_fp16=False,
        )

    def rerank(
        self,
        question: str,
        documents: list[str],
    ):

        pairs = [
            [question, doc]
            for doc in documents
        ]

        scores = self.model.compute_score(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked