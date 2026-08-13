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

    Supports both single-text and batch embedding generation.
    """

    def __init__(self):

        logger.info(
            "Loading embedding model: %s",
            settings.EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        logger.info(
            "Embedding model loaded successfully."
        )

    # ==========================================================
    # Single Embedding
    # ==========================================================

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    # ==========================================================
    # Batch Embeddings
    # ==========================================================

    def generate_embeddings(
        self,
        texts: list[str],
        batch_size: int = 16,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts in batches.

        Batch processing is significantly faster than calling
        generate_embedding() separately for every chunk.
        """

        if not texts:
            return []

        logger.info(
            "Generating embeddings for %d chunks...",
            len(texts),
        )

        logger.info(
            "Embedding batch size: %d",
            batch_size,
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
            "Generated %d embeddings successfully.",
            len(result),
        )

        return result