from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker


retriever = Retriever()
reranker = Reranker()

results = retriever.retrieve(
    "Explain typecasting.",
)

documents = results["documents"][0]

ranked = reranker.rerank(
    query="Explain typecasting.",
    documents=documents,
)

print("=" * 80)

for item in ranked:

    print()

    print(item["score"])

    print(item["document"])