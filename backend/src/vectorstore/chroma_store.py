"""
ChromaDB Vector Store for MVRAG AI.
"""

from __future__ import annotations

import chromadb

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class ChromaStore:

    def __init__(self):

        logger.info("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(settings.vector_db_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.VECTOR_DB_NAME
        )

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ):

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )