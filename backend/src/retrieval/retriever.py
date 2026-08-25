"""
Retriever module for MVRAG AI.

Searches the vector database using semantic similarity.
"""

from __future__ import annotations

from src.config.settings import settings
from src.core.logger import get_logger
from src.embeddings.chroma_store import ChromaStore
from src.embeddings.embedding_generator import EmbeddingGenerator

logger = get_logger(__name__)


class Retriever:
    """Retrieves the most relevant chunks from ChromaDB."""

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.chroma_store = ChromaStore()
        logger.info("Retriever initialized.")

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        video_id: int | None = None,
    ) -> dict:
        """Retrieve top-k similar chunks, optionally for one video."""

        if top_k is None:
            top_k = settings.TOP_K_RESULTS

        logger.info(
            "Searching for: %s | video_id=%s",
            query,
            video_id,
        )

        query_embedding = (
            self.embedding_generator.generate_embedding(query)
        )

        results = self.chroma_store.search(
            embedding=query_embedding,
            top_k=top_k,
            video_id=video_id,
        )

        ids = results.get("ids") or [[]]

        logger.info(
            "Retrieved %d results for video_id=%s.",
            len(ids[0]) if ids else 0,
            video_id,
        )

        return results
