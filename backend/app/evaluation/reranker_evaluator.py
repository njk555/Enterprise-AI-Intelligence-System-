from app.core.database import SessionLocal
from app.retrieval.hybrid import HybridRetrievalService
from app.retrieval.reranker import RerankerService
from app.evaluation.retrieval_dataset import EVALUATION_DATASET


def get_result_key(result):
    document_title = result["document_title"]
    section = result["content"].splitlines()[0].strip()
    return document_title, section


def recall_at_k(results, relevant_sections, k):
    top_results = results[:k]

    retrieved_keys = {
        get_result_key(result)
        for result in top_results
    }

    return any(
        section in retrieved_keys
        for section in relevant_sections
    )


def reciprocal_rank(results, relevant_sections):
    for rank, result in enumerate(results, start=1):
        if get_result_key(result) in relevant_sections:
            return 1 / rank

    return 0.0


def main():
    db = SessionLocal()

    try:
        hybrid_service = HybridRetrievalService()
        reranker_service = RerankerService()

        total = len(EVALUATION_DATASET)

        recall_1 = 0
        recall_3 = 0
        recall_5 = 0
        reciprocal_ranks = []

        for item in EVALUATION_DATASET:
            question = item["question"]
            relevant_sections = item["relevant_sections"]

            candidates = hybrid_service.search(
                db=db,
                query=question,
                top_k=8,
                candidate_k=8,
            )

            results = reranker_service.rerank(
                query=question,
                results=candidates,
                top_k=5,
            )

            if recall_at_k(results, relevant_sections, 1):
                recall_1 += 1

            if recall_at_k(results, relevant_sections, 3):
                recall_3 += 1

            if recall_at_k(results, relevant_sections, 5):
                recall_5 += 1

            rr = reciprocal_rank(
                results,
                relevant_sections,
            )

            reciprocal_ranks.append(rr)

            first_relevant_rank = None

            for rank, result in enumerate(results, start=1):
                if get_result_key(result) in relevant_sections:
                    first_relevant_rank = rank
                    break

            print("\n" + "=" * 80)
            print(f"Question: {question}")
            print(f"Expected: {relevant_sections}")
            print(f"First relevant rank: {first_relevant_rank}")

            for rank, result in enumerate(results, start=1):
                document_title, section = get_result_key(result)

                print(
                    f"  {rank}. "
                    f"{document_title} | "
                    f"{section} "
                    f"(reranker={result['reranker_score']:.6f})"
                )

        mrr = sum(reciprocal_ranks) / total

        print("\n" + "=" * 80)
        print("DOCUMENT-AWARE HYBRID + RERANKER EVALUATION")
        print("=" * 80)

        print(f"Total questions: {total}")
        print(f"Recall@1: {recall_1 / total:.2%}")
        print(f"Recall@3: {recall_3 / total:.2%}")
        print(f"Recall@5: {recall_5 / total:.2%}")
        print(f"MRR:      {mrr:.4f}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
