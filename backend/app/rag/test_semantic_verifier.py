from app.retrieval.reranker import RerankerService


def test_claims():
    evidence = [
        {
            "content": (
                "Enterprise revenue declined during Q4. "
                "Several large customers reduced purchase volumes, "
                "and demand shifted toward smaller deployment sizes."
            )
        }
    ]

    claims = [
        (
            "SUPPORTED",
            "Several large customers reduced their purchase volumes.",
        ),
        (
            "PARAPHRASED",
            "Large customers bought fewer products during Q4.",
        ),
        (
            "CONTRADICTORY",
            "Several large customers increased their purchase volumes.",
        ),
        (
            "OVERSTATED",
            "All large customers completely stopped purchasing products.",
        ),
        (
            "UNSUPPORTED",
            "The company opened a new office in London.",
        ),
    ]

    reranker = RerankerService()

    print("=" * 80)
    print("SEMANTIC CLAIM VERIFICATION TEST")
    print("=" * 80)

    for label, claim in claims:
        results = reranker.rerank(
            query=claim,
            results=evidence,
            top_k=1,
        )

        score = results[0]["reranker_score"]

        print(f"\n[{label}]")
        print(f"Claim: {claim}")
        print(f"Semantic relevance score: {score:.6f}")


if __name__ == "__main__":
    test_claims()
