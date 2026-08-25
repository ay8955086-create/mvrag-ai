"""
ChromaDB vector store for MVRAG AI.
"""

from __future__ import annotations

from functools import lru_cache

from chromadb import PersistentClient

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_chroma_collection():
    logger.info(
        "Initializing ChromaDB at %s",
        settings.vector_db_dir,
    )

    client = PersistentClient(
        path=str(settings.vector_db_dir)
    )

    collection = client.get_or_create_collection(
        name=settings.VECTOR_DB_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    logger.info(
        "ChromaDB collection ready: %s",
        settings.VECTOR_DB_NAME,
    )

    return collection


class ChromaStore:
    """Handles ChromaDB operations."""

    def __init__(self):
        self.collection = get_chroma_collection()

    def add_embeddings(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        if not ids:
            return

        if not (
            len(ids)
            == len(embeddings)
            == len(documents)
            == len(metadatas)
        ):
            raise ValueError(
                "ChromaDB batch data lengths do not match."
            )

        logger.info(
            "Writing %d embeddings to ChromaDB.",
            len(ids),
        )

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info("ChromaDB indexing completed.")

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        video_id: int | None = None,
    ) -> dict:
        """Search vectors, optionally restricted to one video."""

        kwargs = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }

        if video_id is not None:
            kwargs["where"] = {"video_id": int(video_id)}

        try:
            return self.collection.query(**kwargs)
        except Exception:
            logger.exception(
                "ChromaDB search failed for video_id=%s.",
                video_id,
            )
            raise

    def delete_by_video_id(
        self,
        video_id: int,
    ) -> None:
        """Delete vectors belonging to one video."""

        existing = self.collection.get(
            where={"video_id": int(video_id)},
        )

        ids = existing.get("ids") or []

        if ids:
            self.collection.delete(ids=ids)
            logger.info(
                "Deleted %d existing vectors for video %d.",
                len(ids),
                video_id,
            )

    def count(self) -> int:
        return self.collection.count()
