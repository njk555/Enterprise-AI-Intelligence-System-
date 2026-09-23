from app.rag.claim_parser import parse_claims
from app.rag.claim_verifier import verify_claim
from app.rag.semantic_claim_verifier import SemanticClaimVerifier


class ClaimVerificationService:
    """
    Combines lexical evidence verification with semantic
    evidence relevance scoring.

    The semantic model is a reranker, not an NLI model.
    Therefore REVIEW means the evidence relationship is
    ambiguous and should not be treated as a factual failure.
    """

    def __init__(self):
        self.semantic_verifier = (
            SemanticClaimVerifier()
        )

    def verify(
        self,
        structured_output: str,
        evidence: list[dict],
        minimum_overlap: float = 0.20,
    ) -> dict:

        claims = parse_claims(
            structured_output
        )

        if not claims:
            return {
                "valid": False,
                "claims": [],
                "total_claims": 0,
                "supported_claims": 0,
                "review_claims": 0,
                "unsupported_claims": 0,
                "support_rate": 0.0,
                "error": "No claims could be parsed.",
            }

        verified_claims = []

        for claim_data in claims:

            lexical_result = verify_claim(
                claim=claim_data["claim"],
                citations=claim_data["citations"],
                evidence=evidence,
                minimum_overlap=minimum_overlap,
            )

            semantic_result = (
                self.semantic_verifier.score_claim(
                    claim=claim_data["claim"],
                    citations=claim_data["citations"],
                    evidence=evidence,
                )
            )

            lexical_supported = (
                lexical_result["supported"]
            )

            semantic_status = (
                semantic_result["status"]
            )

            if (
                lexical_supported
                and semantic_status
                == "STRONG_EVIDENCE"
            ):
                overall_status = "SUPPORTED"

            elif semantic_status == "LOW_EVIDENCE":
                overall_status = "UNSUPPORTED"

            else:
                overall_status = "REVIEW"

            verified_claims.append({
                **claim_data,
                "lexical_verification": lexical_result,
                "semantic_verification": semantic_result,
                "status": overall_status,
            })

        supported_count = sum(
            1
            for item in verified_claims
            if item["status"] == "SUPPORTED"
        )

        review_count = sum(
            1
            for item in verified_claims
            if item["status"] == "REVIEW"
        )

        unsupported_count = sum(
            1
            for item in verified_claims
            if item["status"] == "UNSUPPORTED"
        )

        total = len(verified_claims)

        return {
            "valid": True,
            "claims": verified_claims,
            "total_claims": total,
            "supported_claims": supported_count,
            "review_claims": review_count,
            "unsupported_claims": unsupported_count,
            "support_rate": (
                supported_count / total
                if total
                else 0.0
            ),
        }


if __name__ == "__main__":

    evidence = [
        {
            "content": (
                "Enterprise revenue declined during Q4. "
                "Several large customers reduced purchase "
                "volumes, and demand shifted toward smaller "
                "deployment sizes."
            )
        },
        {
            "content": (
                "Cloud infrastructure expenditure increased "
                "during Q4 because of higher AI inference, "
                "data processing, storage, and monitoring costs."
            )
        },
    ]

    structured_output = """
CLAIM 1: Several large customers reduced purchase volumes.
EVIDENCE: [1]

CLAIM 2: Infrastructure expenditure increased during Q4.
EVIDENCE: [2]

CLAIM 3: The company opened a new office in London.
EVIDENCE: [1]
"""

    service = ClaimVerificationService()

    result = service.verify(
        structured_output=structured_output,
        evidence=evidence,
    )

    print("=" * 80)
    print("COMBINED CLAIM VERIFICATION TEST")
    print("=" * 80)

    print(
        f"Total claims:       "
        f"{result['total_claims']}"
    )

    print(
        f"Supported claims:   "
        f"{result['supported_claims']}"
    )

    print(
        f"Review claims:      "
        f"{result['review_claims']}"
    )

    print(
        f"Unsupported claims: "
        f"{result['unsupported_claims']}"
    )

    print(
        f"Support rate:       "
        f"{result['support_rate']:.2%}"
    )

    for index, item in enumerate(
        result["claims"],
        start=1,
    ):
        lexical = item[
            "lexical_verification"
        ]

        semantic = item[
            "semantic_verification"
        ]

        print(
            f"\nClaim {index}: "
            f"{item['claim']}"
        )

        print(
            f"Evidence: "
            f"{item['citations']}"
        )

        print(
            f"Lexical overlap: "
            f"{lexical['overlap']:.2%}"
        )

        print(
            f"Semantic score: "
            f"{semantic['semantic_score']:.6f}"
        )

        print(
            f"Semantic status: "
            f"{semantic['status']}"
        )

        print(
            f"Overall status: "
            f"{item['status']}"
        )
