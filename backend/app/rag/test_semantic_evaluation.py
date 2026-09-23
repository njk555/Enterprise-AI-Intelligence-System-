from app.retrieval.reranker import RerankerService


EVIDENCE = [
    {
        "content": (
            "Enterprise revenue declined during Q4. "
            "Several large customers reduced purchase volumes, "
            "and demand shifted toward smaller deployment sizes. "
            "Average order quantities declined, particularly in "
            "Enterprise Analytics and Customer Intelligence."
        )
    }
]


TEST_CASES = [
    (
        "SUPPORTED",
        "Several large customers reduced their purchase volumes.",
    ),
    (
        "SUPPORTED",
        "Average order quantities declined during Q4.",
    ),
    (
        "SUPPORTED",
        "Demand moved toward smaller deployment sizes.",
    ),
    (
        "PARAPHRASED",
        "Large customers bought fewer products during Q4.",
    ),
    (
        "PARAPHRASED",
        "Customers increasingly chose smaller deployments.",
    ),
    (
        "PARAPHRASED",
        "Enterprise Analytics and Customer Intelligence experienced lower order quantities.",
    ),
    (
        "CONTRADICTORY",
        "Several large customers increased their purchase volumes.",
    ),
    (
        "CONTRADICTORY",
        "Average order quantities increased during Q4.",
    ),
    (
        "CONTRADICTORY",
        "Customer demand shifted toward larger deployments.",
    ),
    (
        "OVERSTATED",
        "All large customers completely stopped purchasing products.",
    ),
    (
        "OVERSTATED",
        "Every customer moved to the smallest possible deployment.",
    ),
    (
        "OVERSTATED",
        "Enterprise Analytics completely lost all customers.",
    ),
    (
        "UNSUPPORTED",
        "The company opened a new office in London.",
    ),
    (
        "UNSUPPORTED",
        "The company hired 500 new employees.",
    ),
    (
        "UNSUPPORTED",
        "Nexora acquired a competitor in Germany.",
    ),
]


def main():
    reranker = RerankerService()

    results = []

    print("=" * 80)
    print("SEMANTIC VERIFICATION EVALUATION")
    print("=" * 80)

    for label, claim in TEST_CASES:
        ranked = reranker.rerank(
            query=claim,
            results=EVIDENCE,
            top_k=1,
        )

        score = ranked[0]["reranker_score"]

        results.append({
            "label": label,
            "claim": claim,
            "score": score,
        })

        print(f"\n[{label}]")
        print(f"Claim: {claim}")
        print(f"Score: {score:.6f}")

    print("\n" + "=" * 80)
    print("SUMMARY BY CATEGORY")
    print("=" * 80)

    categories = [
        "SUPPORTED",
        "PARAPHRASED",
        "CONTRADICTORY",
        "OVERSTATED",
        "UNSUPPORTED",
    ]

    for category in categories:
        scores = [
            item["score"]
            for item in results
            if item["label"] == category
        ]

        if not scores:
            continue

        print(
            f"{category:<15} "
            f"min={min(scores):.6f} "
            f"max={max(scores):.6f} "
            f"avg={sum(scores) / len(scores):.6f}"
        )


if __name__ == "__main__":
    main()
