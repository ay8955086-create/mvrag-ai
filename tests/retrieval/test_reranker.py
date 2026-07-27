from src.reranker.bge_reranker import BGEReranker

reranker = BGEReranker()

question = "What is Machine Learning?"

documents = [
    "Machine Learning is a branch of Artificial Intelligence.",
    "Football is a popular sport.",
    "Deep Learning is a subset of Machine Learning.",
]

results = reranker.rerank(
    question,
    documents,
)

for doc, score in results:
    print(score)
    print(doc)
    print()