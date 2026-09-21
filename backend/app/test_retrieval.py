from app.core.database import SessionLocal
from app.retrieval.service import RetrievalService


def main():
    db = SessionLocal()

    try:
        retrieval_service = RetrievalService()

        queries = [
            "Why did enterprise revenue decline during Q4?",
            "What happened to cloud infrastructure costs?",
            "What problems were customers reporting?",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            results = retrieval_service.search(
                db=db,
                query=query,
                top_k=3,
            )

            for rank, result in enumerate(results, start=1):
                print(f"\nRank: {rank}")
                print(f"Chunk ID: {result['chunk_id']}")
                print(f"Document: {result['document_title']}")
                print(f"Distance: {result['distance']:.6f}")
                print(f"Content:\n{result['content'][:500]}")

    finally:
        db.close()


if __name__ == "__main__":
    main()