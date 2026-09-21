from app.core.database import SessionLocal
from app.rag.pipeline import RAGPipeline


def main():
    db = SessionLocal()

    try:
        pipeline = RAGPipeline()

        question = (
            "Why did enterprise revenue decline during Q4?"
        )

        result = pipeline.answer(
            db=db,
            question=question,
        )

        print("\n" + "=" * 80)
        print("RAG ANSWER")
        print("=" * 80)
        print(result["answer"])

        print("\n" + "=" * 80)
        print("CITATION VALIDATION")
        print("=" * 80)
        print(result["citation_validation"])

        print("\n" + "=" * 80)
        print("GROUNDING EVALUATION")
        print("=" * 80)

        grounding = result["grounding"]

        print(
            f"Supported: {grounding['supported']}"
        )
        print(
            f"Overlap:   {grounding['overlap']:.2%}"
        )

        print("\n" + "=" * 80)
        print("STRUCTURED CLAIM OUTPUT")
        print("=" * 80)
        print(
            result["structured_claim_output"]
        )

        print("\n" + "=" * 80)
        print("CLAIM-LEVEL VERIFICATION")
        print("=" * 80)

        verification = (
            result["claim_verification"]
        )

        print(
            f"Valid:              "
            f"{verification['valid']}"
        )

        print(
            f"Total claims:       "
            f"{verification['total_claims']}"
        )

        print(
            f"Supported claims:   "
            f"{verification['supported_claims']}"
        )

        print(
            f"Unsupported claims: "
            f"{verification['unsupported_claims']}"
        )

        print(
            f"Support rate:       "
            f"{verification['support_rate']:.2%}"
        )

        print("\nCLAIMS")

        for index, item in enumerate(
            verification["claims"],
            start=1,
        ):
            claim_result = (
                item["verification"]
            )

            print(
                f"\nClaim {index}: "
                f"{item['claim']}"
            )

            print(
                f"Evidence: "
                f"{item['citations']}"
            )

            print(
                f"Supported: "
                f"{claim_result['supported']}"
            )

            print(
                f"Overlap: "
                f"{claim_result['overlap']:.2%}"
            )

        print("\n" + "=" * 80)
        print("RETRIEVED EVIDENCE")
        print("=" * 80)

        for index, evidence in enumerate(
            result["evidence"],
            start=1,
        ):
            section = (
                evidence["content"]
                .splitlines()[0]
                .strip()
            )

            print(
                f"\n[{index}] {section}"
            )

            print(
                f"Document: "
                f"{evidence['document_title']}"
            )

            print(
                f"Reranker score: "
                f"{evidence['reranker_score']:.6f}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
