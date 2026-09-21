from sqlalchemy.orm import Session

from app.retrieval.hybrid import HybridRetrievalService
from app.retrieval.reranker import RerankerService

from app.rag.prompt import build_rag_prompt
from app.rag.citation_validator import validate_citations
from app.rag.claim_verification_service import ClaimVerificationService

from app.evaluation.grounding import answer_supported_by_evidence

from app.llm.groq_service import GroqLLMService


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.

    Flow:

        Question
        -> Hybrid Retrieval
        -> Cross-Encoder Reranking
        -> Evidence Selection
        -> LLM Answer Generation
        -> Citation Validation
        -> Grounding Evaluation
        -> Atomic Claim Generation
        -> Claim Parsing
        -> Claim-Level Verification
    """

    def __init__(self):
        self.hybrid_service = HybridRetrievalService()
        self.reranker_service = RerankerService()
        self.llm_service = GroqLLMService()
        self.claim_verification_service = (
            ClaimVerificationService()
        )

    def _build_claim_prompt(
        self,
        question: str,
        evidence: list[dict],
    ) -> str:
        """
        Build a structured prompt that asks the LLM
        to break the answer into atomic factual claims.
        """

        evidence_blocks = []

        for index, result in enumerate(
            evidence,
            start=1,
        ):
            section = result["content"].splitlines()[0].strip()

            evidence_blocks.append(
                f"[{index}] {section}\n"
                f"{result['content']}"
            )

        evidence_text = "\n\n".join(
            evidence_blocks
        )

        return f"""
You are an enterprise evidence extraction system.

Analyze the user's question and the provided evidence.

Return ONLY atomic factual claims supported by the evidence.

Use EXACTLY this format:

CLAIM 1: <one atomic factual claim>
EVIDENCE: [1]

CLAIM 2: <one atomic factual claim>
EVIDENCE: [2]

Rules:

- Break the answer into atomic factual claims.
- Each claim must express only ONE independently verifiable fact.
- Every factual claim must have at least one evidence reference.
- Do not combine multiple independent facts into one claim.
- Do not use outside knowledge.
- Do not invent or assume facts.
- Use only evidence references that exist.
- If multiple evidence items support one claim, cite all relevant references.
- Do not add explanations outside the required format.

EVIDENCE:

{evidence_text}

USER QUESTION:

{question}
""".strip()

    def answer(
        self,
        db: Session,
        question: str,
        retrieval_k: int = 8,
        evidence_k: int = 3,
    ) -> dict:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # --------------------------------------------------
        # 1. Hybrid Retrieval
        # --------------------------------------------------

        candidates = self.hybrid_service.search(
            db=db,
            query=question,
            top_k=retrieval_k,
            candidate_k=retrieval_k,
        )

        # --------------------------------------------------
        # 2. Cross-Encoder Reranking
        # --------------------------------------------------

        reranked_results = self.reranker_service.rerank(
            query=question,
            results=candidates,
            top_k=evidence_k,
        )

        # --------------------------------------------------
        # 3. Generate Final Answer
        # --------------------------------------------------

        prompt = build_rag_prompt(
            question=question,
            results=reranked_results,
        )

        answer = self.llm_service.generate(
            prompt=prompt,
        )

        # --------------------------------------------------
        # 4. Citation Validation
        # --------------------------------------------------

        citation_validation = validate_citations(
            answer=answer,
            evidence_count=len(reranked_results),
            require_citation=True,
        )

        # --------------------------------------------------
        # 5. Lexical Grounding
        # --------------------------------------------------

        grounding = answer_supported_by_evidence(
            answer=answer,
            evidence=reranked_results,
        )

        # --------------------------------------------------
        # 6. Generate Atomic Claims
        # --------------------------------------------------

        claim_prompt = self._build_claim_prompt(
            question=question,
            evidence=reranked_results,
        )

        structured_claim_output = (
            self.llm_service.generate(
                prompt=claim_prompt,
            )
        )

        # --------------------------------------------------
        # 7. Claim-Level Verification
        # --------------------------------------------------

        claim_verification = (
            self.claim_verification_service.verify(
                structured_output=structured_claim_output,
                evidence=reranked_results,
            )
        )

        # --------------------------------------------------
        # 8. Final Result
        # --------------------------------------------------

        return {
            "question": question,
            "answer": answer,

            "evidence": reranked_results,

            "citation_validation": citation_validation,

            "grounding": grounding,

            "structured_claim_output": (
                structured_claim_output
            ),

            "claim_verification": (
                claim_verification
            ),
        }
