from app.core.database import SessionLocal
from app.retrieval.hybrid import HybridRetrievalService

def main():
    db = SessionLocal()

    try:
        service = HybridRetrievalService()

        query = "What were the most common customer support issues?"

        results = service.search(
            db=db,
            query=query,
            top_k=10,
            candidate_k=20,
        )

        print("\n" + "=" * 90)
        print("HYBRID RETRIEVAL DIAGNOSTIC")
        print("=" * 90)
        print(f"Query: {query}\n")

        for rank, result in enumerate(results, start=1):
            section = result["content"].splitlines()[0].strip()

            print(
                f"{rank}. "
                f"{result['document_title']} | "
                f"{section}"
            )
            print(
                f"   RRF score:     {result['rrf_score']:.6f}"
            )
            print(
                f"   Vector rank:   {result['vector_rank']}"
            )
            print(
                f"   Keyword rank:  {result['keyword_rank']}"
            )
            print()

    finally:
        db.close()


if __name__ == "__main__":
    main()
