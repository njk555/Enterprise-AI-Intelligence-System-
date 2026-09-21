from app.llm.groq_service import GroqLLMService


def main():
    llm = GroqLLMService()

    prompt = """
You are an enterprise evidence extraction system.

Answer the question using ONLY the evidence provided.

Return EXACTLY this format:

CLAIM 1: <one atomic factual claim>
EVIDENCE: [1]

CLAIM 2: <one atomic factual claim>
EVIDENCE: [2]

Rules:
- Break the answer into atomic factual claims.
- Each claim must express only ONE independently verifiable fact.
- Every factual claim must have at least one evidence reference.
- Do not combine multiple facts into one claim.
- Do not use outside knowledge.
- Do not invent or assume facts.
- Use only evidence references that exist.
- If multiple evidence items support one claim, cite all of them.
- Do not add explanations outside the required format.

EVIDENCE:

[1] Revenue Performance
Enterprise revenue declined during Q4. Several large customers reduced purchase volumes, and demand shifted toward smaller deployment sizes. Average order quantities declined, particularly in Enterprise Analytics and Customer Intelligence.

[2] Infrastructure Costs
Cloud infrastructure expenditure increased during Q4 because of higher AI inference, data processing, storage, and monitoring costs.

QUESTION:

Why did enterprise revenue decline during Q4?
"""

    response = llm.generate(prompt)

    print("\n" + "=" * 80)
    print("ATOMIC CLAIM OUTPUT TEST")
    print("=" * 80)
    print(response)


if __name__ == "__main__":
    main()
