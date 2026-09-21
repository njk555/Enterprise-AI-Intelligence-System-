import re


def parse_claims(text: str) -> list[dict]:
    """
    Parse structured claims produced by the LLM.

    Expected format:

    CLAIM 1: Some factual claim.
    EVIDENCE: [1]

    CLAIM 2: Another factual claim.
    EVIDENCE: [1] [2]
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    claims = []
    current_claim = None

    for line in lines:
        if line.upper().startswith("CLAIM "):
            if current_claim is not None:
                claims.append(current_claim)

            claim_text = line.split(":", 1)

            if len(claim_text) != 2:
                continue

            current_claim = {
                "claim": claim_text[1].strip(),
                "citations": [],
            }

        elif line.upper().startswith("EVIDENCE:"):
            if current_claim is None:
                continue

            evidence_text = line.split(":", 1)[1]

            citations = re.findall(
                r"\[(\d+)\]",
                evidence_text,
            )

            current_claim["citations"] = [
                int(citation)
                for citation in citations
            ]

    if current_claim is not None:
        claims.append(current_claim)

    return claims


if __name__ == "__main__":
    sample = """
CLAIM 1: Large customers reduced purchase volumes.
EVIDENCE: [1]

CLAIM 2: Demand shifted toward smaller deployment sizes.
EVIDENCE: [1]

CLAIM 3: Average order quantities declined.
EVIDENCE: [1]

CLAIM 4: Orders in Enterprise Analytics and Customer Intelligence declined.
EVIDENCE: [1]
"""

    parsed = parse_claims(sample)

    for index, claim in enumerate(parsed, start=1):
        print(f"Claim {index}:")
        print(f"  Text: {claim['claim']}")
        print(f"  Evidence: {claim['citations']}")
        print()
