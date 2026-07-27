"""
Semantic Retriever for MVRAG AI.
"""

from __future__ import annotations

from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.chroma_store import ChromaStore


class Retriever:

    def __init__(self):

        self.embedder = EmbeddingGenerator()
        self.store = ChromaStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        query_embedding = self.embedder.generate_embedding(question)

        results = self.store.search(
            embedding=query_embedding,
            top_k=top_k,
        )

        return results