"""
ChromaDB vector store for MVRAG AI.
"""

from __future__ import annotations

from chromadb import PersistentClient

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class ChromaStore:
    """
    Handles all interactions with ChromaDB.
    """

    def __init__(self):

        logger.info(
            "Initializing ChromaDB at %s",
            settings.vector_db_dir,
        )

        self.client = PersistentClient(
            path=str(
                settings.vector_db_dir
            ),
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=settings.VECTOR_DB_NAME,
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

        logger.info(
            "Collection '%s' ready.",
            settings.VECTOR_DB_NAME,
        )

    # ==========================================================
    # Add Single Embedding
    # ==========================================================

    def add_embedding(
        self,
        embedding_id: str,
        embedding: list[float],
        document: str,
        metadata: dict,
    ) -> None:
        """
        Store a single embedding.
        """

        self.collection.add(
            ids=[embedding_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata],
        )

    # ==========================================================
    # Add Multiple Embeddings
    # ==========================================================

    def add_embeddings(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        """
        Store multiple embeddings in one ChromaDB operation.
        """

        if not ids:
            logger.info(
                "No embeddings to store."
            )
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
            "Writing %d embeddings to ChromaDB...",
            len(ids),
        )

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info(
            "Successfully stored %d embeddings in ChromaDB.",
            len(ids),
        )

    # ==========================================================
    # Search
    # ==========================================================

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> dict:
        """
        Search the vector database.
        """

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )