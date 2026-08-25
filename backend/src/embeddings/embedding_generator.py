"""
Embedding Generator for MVRAG AI.
"""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """

    logger.info(
        "Loading embedding model: %s",
        settings.EMBEDDING_MODEL,
    )

    model = SentenceTransformer(
        settings.EMBEDDING_MODEL
    )

    logger.info(
        "Embedding model loaded successfully."
    )

    return model


class EmbeddingGenerator:
    """
    Generates embeddings using BGE.
    """

    def __init__(self):

        self.model = get_embedding_model()

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
        batch_size: int = 16,
    ) -> list[list[float]]:

        if not texts:
            return []

        logger.info(
            "Generating embeddings for %d chunks.",
            len(texts),
        )

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        result = embeddings.tolist()

        logger.info(
            "Generated %d embeddings.",
            len(result),
        )

        return result