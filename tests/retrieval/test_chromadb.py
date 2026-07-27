from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.chroma_store import ChromaStore

embedder = EmbeddingGenerator()
store = ChromaStore()

text = """
Transcript:
Machine Learning

OCR:
Machine Learning

Caption:
Teacher explaining ML.
"""

embedding = embedder.generate_embedding(text)

store.add(
    ids=["chunk_1"],
    embeddings=[embedding],
    documents=[text],
    metadatas=[
        {
            "video_id": 1,
            "chunk_index": 0,
            "start_time": 0,
            "end_time": 10,
        }
    ],
)

result = store.search(
    embedding,
)

print(result)