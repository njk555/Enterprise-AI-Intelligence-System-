from app.core.database import SessionLocal
from app.retrieval.hybrid import HybridRetrievalService
from app.retrieval.reranker import RerankerService
from app.rag.prompt import build_rag_prompt


def main():
    db = SessionLocal()

    try:
        question = "Why did enterprise revenue decline during Q4?"

        hybrid_service = HybridRetrievalService()
        reranker_service = RerankerService()

        candidates = hybrid_service.search(
            db=db,
            query=question,
            top_k=8,
            candidate_k=8,
        )

        results = reranker_service.rerank(
            query=question,
            results=candidates,
            top_k=3,
        )

        prompt = build_rag_prompt(
            question=question,
            results=results,
        )

        print("\n" + "=" * 80)
        print("GENERATED RAG PROMPT")
        print("=" * 80)
        print(prompt)

    finally:
        db.close()


if __name__ == "__main__":
    main()
