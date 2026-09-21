from app.core.database import SessionLocal
from app.retrieval.hybrid import HybridRetrievalService
from app.retrieval.reranker import RerankerService


def main():
    db = SessionLocal()

    try:
        hybrid_service = HybridRetrievalService()
        reranker_service = RerankerService()

        queries = [
            "Why did enterprise revenue decline during Q4?",
            "What were the most common customer support issues?",
            "Why were customers experiencing dashboard performance problems?",
            "What caused the increase in infrastructure expenditure?",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            candidates = hybrid_service.search(
                db=db,
                query=query,
                top_k=8,
                candidate_k=20,
            )

            results = reranker_service.rerank(
                query=query,
                results=candidates,
                top_k=5,
            )

            for rank, result in enumerate(results, start=1):
                section = result["content"].splitlines()[0].strip()

                print(
                    f"{rank}. "
                    f"{result['document_title']} | "
                    f"{section} | "
                    f"score={result['reranker_score']:.6f}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
