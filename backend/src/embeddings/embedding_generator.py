"""
Embedding Generator for MVRAG AI.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings using the configured BGE model.
    """

    def __init__(self):

        logger.info(
            "Loading embedding model: %s",
            settings.EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()