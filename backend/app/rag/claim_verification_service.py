from app.rag.claim_parser import parse_claims
from app.rag.claim_verifier import verify_claims


class ClaimVerificationService:
    """
    Converts structured LLM claim output into independently
    verified factual claims.
    """

    def verify(
        self,
        structured_output: str,
        evidence: list[dict],
        minimum_overlap: float = 0.20,
    ) -> dict:
        claims = parse_claims(structured_output)

        if not claims:
            return {
                "valid": False,
                "claims": [],
                "total_claims": 0,
                "supported_claims": 0,
                "unsupported_claims": 0,
                "support_rate": 0.0,
                "error": "No claims could be parsed.",
            }

        verified_claims = verify_claims(
            claims=claims,
            evidence=evidence,
            minimum_overlap=minimum_overlap,
        )

        supported_count = sum(
            1
            for item in verified_claims
            if item["verification"]["supported"]
        )

        unsupported_count = (
            len(verified_claims) - supported_count
        )

        support_rate = (
            supported_count / len(verified_claims)
        )

        return {
            "valid": True,
            "claims": verified_claims,
            "total_claims": len(verified_claims),
            "supported_claims": supported_count,
            "unsupported_claims": unsupported_count,
            "support_rate": support_rate,
        }


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

    structured_output = """
CLAIM 1: Large customers reduced purchase volumes.
EVIDENCE: [1]

CLAIM 2: Demand shifted toward smaller deployment sizes.
EVIDENCE: [1]

CLAIM 3: The company opened an office in London.
EVIDENCE: [1]
"""

    service = ClaimVerificationService()

    result = service.verify(
        structured_output=structured_output,
        evidence=evidence,
    )

    print("=" * 80)
    print("CLAIM VERIFICATION SERVICE TEST")
    print("=" * 80)

    print(f"Total claims:       {result['total_claims']}")
    print(f"Supported claims:   {result['supported_claims']}")
    print(f"Unsupported claims: {result['unsupported_claims']}")
    print(f"Support rate:       {result['support_rate']:.2%}")

    print("\nCLAIMS")

    for index, item in enumerate(
        result["claims"],
        start=1,
    ):
        verification = item["verification"]

        print(f"\nClaim {index}:")
        print(f"  {item['claim']}")
        print(f"  Evidence: {item['citations']}")
        print(
            f"  Supported: {verification['supported']}"
        )
        print(
            f"  Overlap: {verification['overlap']:.2%}"
        )
