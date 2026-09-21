import re


def normalize_text(text: str) -> str:
    """
    Normalize text for simple lexical comparison.
    """

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def answer_supported_by_evidence(
    answer: str,
    evidence: list[dict],
    minimum_overlap: float = 0.20,
) -> dict:
    """
    Perform a simple lexical grounding check.

    This is an initial deterministic evaluator, not a semantic
    or LLM-based faithfulness judge.
    """

    if not answer.strip():
        return {
            "supported": False,
            "overlap": 0.0,
        }

    evidence_text = " ".join(
        item["content"]
        for item in evidence
    )

    answer_words = set(
        normalize_text(answer).split()
    )

    evidence_words = set(
        normalize_text(evidence_text).split()
    )

    if not answer_words:
        return {
            "supported": False,
            "overlap": 0.0,
        }

    overlap_words = answer_words & evidence_words

    overlap = len(overlap_words) / len(answer_words)

    return {
        "supported": overlap >= minimum_overlap,
        "overlap": overlap,
        "overlap_words": sorted(overlap_words),
    }
