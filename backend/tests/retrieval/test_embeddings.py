from src.embeddings.embedding_generator import EmbeddingGenerator

generator = EmbeddingGenerator()

text = """
Transcript:
Today we study Machine Learning.

OCR:
Machine Learning

Caption:
Teacher explaining concepts on a whiteboard.
"""

embedding = generator.generate_embedding(text)

print()

print("Embedding Dimension :", len(embedding))

print()

print("First 10 values")

print(embedding[:10])