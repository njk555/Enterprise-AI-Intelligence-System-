import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def verify_claim(
    claim: str,
    citations: list[int],
    evidence: list[dict],
    minimum_overlap: float = 0.20,
) -> dict:
    """
    Verify whether a claim has sufficient lexical overlap
    with the evidence it cites.
    """

    if not claim.strip():
        return {
            "supported": False,
            "overlap": 0.0,
            "reason": "Empty claim.",
        }

    if not citations:
        return {
            "supported": False,
            "overlap": 0.0,
            "reason": "No evidence citation provided.",
        }

    cited_evidence = []

    for citation in citations:
        index = citation - 1

        if 0 <= index < len(evidence):
            cited_evidence.append(
                evidence[index]["content"]
            )

    if not cited_evidence:
        return {
            "supported": False,
            "overlap": 0.0,
            "reason": "All cited evidence references are invalid.",
        }

    claim_words = set(
        normalize_text(claim).split()
    )

    evidence_words = set(
        normalize_text(
            " ".join(cited_evidence)
        ).split()
    )

    if not claim_words:
        return {
            "supported": False,
            "overlap": 0.0,
            "reason": "Claim contains no usable words.",
        }

    overlap_words = claim_words & evidence_words

    overlap = len(overlap_words) / len(claim_words)

    return {
        "supported": overlap >= minimum_overlap,
        "overlap": overlap,
        "overlap_words": sorted(overlap_words),
        "reason": (
            "Sufficient lexical overlap."
            if overlap >= minimum_overlap
            else "Insufficient lexical overlap."
        ),
    }


def verify_claims(
    claims: list[dict],
    evidence: list[dict],
    minimum_overlap: float = 0.20,
) -> list[dict]:
    """
    Verify every claim independently.
    """

    results = []

    for claim_data in claims:
        verification = verify_claim(
            claim=claim_data["claim"],
            citations=claim_data["citations"],
            evidence=evidence,
            minimum_overlap=minimum_overlap,
        )

        results.append({
            **claim_data,
            "verification": verification,
        })

    return results


if __name__ == "__main__":
    evidence = [
        {
            "content": (
                "Enterprise revenue declined during Q4. "
                "Several large customers reduced purchase volumes, "
                "and demand shifted toward smaller deployment sizes. "
                "Average order quantities declined, particularly in "
                "Enterprise Analytics and Customer Intelligence."
            )
        },
        {
            "content": (
                "Cloud infrastructure expenditure increased during Q4 "
                "because of higher AI inference, data processing, "
                "storage, and monitoring costs."
            )
        },
    ]

    claims = [
        {
            "claim": "Large customers reduced purchase volumes.",
            "citations": [1],
        },
        {
            "claim": "Demand shifted toward smaller deployment sizes.",
            "citations": [1],
        },
        {
            "claim": "Average order quantities declined.",
            "citations": [1],
        },
        {
            "claim": "Orders in Enterprise Analytics and Customer Intelligence declined.",
            "citations": [1],
        },
        {
            "claim": "The company opened an office in London.",
            "citations": [1],
        },
    ]

    results = verify_claims(
        claims=claims,
        evidence=evidence,
    )

    print("=" * 80)
    print("CLAIM-LEVEL VERIFICATION TEST")
    print("=" * 80)

    for index, result in enumerate(results, start=1):
        verification = result["verification"]

        print(f"\nClaim {index}: {result['claim']}")
        print(f"Evidence: {result['citations']}")
        print(
            f"Supported: {verification['supported']}"
        )
        print(
            f"Overlap:   {verification['overlap']:.2%}"
        )
        print(
            f"Reason:    {verification['reason']}"
        )
