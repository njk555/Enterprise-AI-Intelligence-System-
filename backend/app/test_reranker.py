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
            "Which product lines were most affected by the Q4 decline?",
            "Which customers reduced their purchases or deployment volume?",
            "What problems were customers reporting?",
            "What were the most common support issues?",
            "Why did cloud infrastructure expenditure increase?",
            "What caused the increase in AI infrastructure costs?",
            "What actions did management recommend?",
            "What risks does Nexora face in FY2026?",
            "How did enterprise order volume change during Q4?",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            candidates = hybrid_service.search(
                db=db,
                query=query,
                top_k=5,
                candidate_k=8,
            )

            results = reranker_service.rerank(
                query=query,
                results=candidates,
                top_k=5,
            )

            for rank, result in enumerate(results, start=1):
                section = result["content"].splitlines()[0].strip()

                print(
                    f"{rank}. {section} "
                    f"| Reranker: "
                    f"{result['reranker_score']:.6f} "
                    f"| RRF: "
                    f"{result['rrf_score']:.6f}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
