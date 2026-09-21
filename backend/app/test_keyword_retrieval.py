from app.core.database import SessionLocal
from app.retrieval.keyword import KeywordRetrievalService


def main():
    db = SessionLocal()

    try:
        service = KeywordRetrievalService()

        queries = [
            "enterprise revenue decline",
            "cloud infrastructure costs",
            "API timeouts dashboard performance",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            results = service.search(
                db=db,
                query=query,
                top_k=3,
            )

            if not results:
                print("No keyword matches found.")
                continue

            for rank, result in enumerate(results, start=1):
                print(f"\nRank: {rank}")
                print(f"Chunk ID: {result['chunk_id']}")
                print(f"Section/content preview:")
                print(result["content"][:500])
                print(f"Keyword score: {result['score']:.6f}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
