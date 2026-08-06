from src.retrieval.retriever import Retriever


retriever = Retriever()

results = retriever.retrieve(
    "Explain typecasting.",
)

print("=" * 70)

print(results)