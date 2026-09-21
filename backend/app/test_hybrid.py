from app.core.database import SessionLocal
from app.retrieval.hybrid import HybridRetrievalService


def main():
    db = SessionLocal()

    try:
        service = HybridRetrievalService()

        queries = [
            "Why did enterprise revenue decline during Q4?",
            "What happened to cloud infrastructure costs?",
            "What problems were customers reporting?",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            results = service.search(
                db=db,
                query=query,
                top_k=3,
                candidate_k=8,
            )

            for rank, result in enumerate(results, start=1):
                print(f"\nFinal Rank: {rank}")
                print(f"Chunk ID: {result['chunk_id']}")
                print(f"Section: {result['content'].splitlines()[0]}")
                print(f"Vector Rank: {result.get('vector_rank')}")
                print(f"Keyword Rank: {result.get('keyword_rank')}")
                print(f"RRF Score: {result['rrf_score']:.6f}")
                print(f"Content Preview:\n{result['content'][:400]}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
