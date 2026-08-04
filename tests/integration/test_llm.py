from src.pipeline.query_pipeline import QueryPipeline

pipeline = QueryPipeline()

result = pipeline.process_query(
    "Explain explicit typecasting."
)

print("=" * 80)
print("QUESTION")
print("=" * 80)
print(result["question"])

print()

print("=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print()

print("=" * 80)
print("RETRIEVED CONTEXT")
print("=" * 80)

for index, item in enumerate(result["context"], start=1):

    print(f"\nResult {index}")
    print("-" * 50)
    print(item["score"])
    print(item["document"])