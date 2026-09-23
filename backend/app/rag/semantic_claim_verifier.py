from app.retrieval.reranker import RerankerService


class SemanticClaimVerifier:
    """
    Measures semantic relevance between a claim and each piece
    of evidence explicitly cited by that claim.

    BGE reranker is a relevance model, not an NLI/entailment model.
    Therefore the scores indicate evidence relevance, not formal
    factual entailment.
    """

    def __init__(self):
        self.reranker = RerankerService()

    def score_claim(
        self,
        claim: str,
        citations: list[int],
        evidence: list[dict],
    ) -> dict:

        if not claim.strip():
            raise ValueError("Claim cannot be empty.")

        if not citations:
            return {
                "semantic_score": 0.0,
                "status": "UNSUPPORTED",
                "evidence_scores": [],
                "reason": "No evidence citations provided.",
            }

        cited_evidence = []

        for citation in citations:
            index = citation - 1

            if 0 <= index < len(evidence):
                cited_evidence.append(
                    {
                        "citation": citation,
                        "content": evidence[index]["content"],
                    }
                )

        if not cited_evidence:
            return {
                "semantic_score": 0.0,
                "status": "UNSUPPORTED",
                "evidence_scores": [],
                "reason": "All evidence citations are invalid.",
            }

        evidence_scores = []

        for item in cited_evidence:
            result = self.reranker.rerank(
                query=claim,
                results=[
                    {
                        "content": item["content"],
                    }
                ],
                top_k=1,
            )

            score = result[0]["reranker_score"]

            evidence_scores.append(
                {
                    "citation": item["citation"],
                    "score": score,
                }
            )

        best_score = max(
            item["score"]
            for item in evidence_scores
        )

        if best_score >= 0.90:
            status = "STRONG_EVIDENCE"
        elif best_score >= 0.50:
            status = "WEAK_OR_AMBIGUOUS"
        else:
            status = "LOW_EVIDENCE"

        return {
            "semantic_score": best_score,
            "status": status,
            "evidence_scores": evidence_scores,
            "reason": (
                "At least one cited evidence item has strong "
                "semantic relevance."
                if status == "STRONG_EVIDENCE"
                else
                "The cited evidence is semantically related, "
                "but relevance alone does not establish entailment."
                if status == "WEAK_OR_AMBIGUOUS"
                else
                "The cited evidence has weak semantic relevance "
                "to the claim."
            ),
        }


if __name__ == "__main__":
    verifier = SemanticClaimVerifier()

    evidence = [
        {
            "content": (
                "Enterprise revenue declined during Q4. "
                "Several large customers reduced purchase volumes, "
                "and demand shifted toward smaller deployment sizes."
            )
        },
        {
            "content": (
                "Cloud infrastructure expenditure increased during Q4 "
                "because of higher AI inference, data processing, "
                "storage, and monitoring costs."
            )
        },
        {
            "content": (
                "The Q4 decline was driven by reduced customer usage "
                "and increasing infrastructure costs."
            )
        },
    ]

    tests = [
        {
            "claim": (
                "Enterprise revenue declined during Q4."
            ),
            "citations": [1, 3],
        },
        {
            "claim": (
                "Infrastructure expenditure increased during Q4."
            ),
            "citations": [2],
        },
        {
            "claim": (
                "The company opened an office in London."
            ),
            "citations": [1],
        },
    ]

    print("=" * 80)
    print("MULTI-EVIDENCE SEMANTIC CLAIM VERIFIER TEST")
    print("=" * 80)

    for test in tests:
        result = verifier.score_claim(
            claim=test["claim"],
            citations=test["citations"],
            evidence=evidence,
        )

        print(f"\nClaim: {test['claim']}")
        print(f"Citations: {test['citations']}")

        for item in result["evidence_scores"]:
            print(
                f"Evidence [{item['citation']}]: "
                f"{item['score']:.6f}"
            )

        print(
            f"Best score: "
            f"{result['semantic_score']:.6f}"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        print(
            f"Reason: "
            f"{result['reason']}"
        )
