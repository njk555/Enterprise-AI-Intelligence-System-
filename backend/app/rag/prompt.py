def build_rag_prompt(
    question: str,
    results: list[dict],
) -> str:
    """
    Build a grounded RAG prompt from retrieved evidence.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not results:
        raise ValueError("At least one evidence result is required.")

    evidence_blocks = []

    for index, result in enumerate(results, start=1):
        section = result["content"].splitlines()[0].strip()
        content = result["content"]

        evidence_blocks.append(
            f"[{index}] {section}\n{content}"
        )

    evidence = "\n\n".join(evidence_blocks)

    return f"""You are an enterprise intelligence assistant.

Answer the user's question using ONLY the evidence provided below.

Rules:
- Do not use outside knowledge.
- Do not invent or assume facts.
- If the evidence is insufficient to answer the question, say so.
- Keep the answer concise but informative.
- Cite the evidence using its reference number, such as [1] or [2].
- When multiple pieces of evidence support an answer, cite all relevant references.

EVIDENCE:

{evidence}

USER QUESTION:

{question}

ANSWER:
"""
