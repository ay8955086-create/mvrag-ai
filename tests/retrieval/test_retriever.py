from src.retrieval.retriever import Retriever

retriever = Retriever()

question = "What is Machine Learning?"

results = retriever.retrieve(question)

print(results)