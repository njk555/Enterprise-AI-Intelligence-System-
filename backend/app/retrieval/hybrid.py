from sqlalchemy.orm import Session

from app.retrieval.service import RetrievalService
from app.retrieval.keyword import KeywordRetrievalService


class HybridRetrievalService:

    def __init__(self):
        self.vector_service = RetrievalService()
        self.keyword_service = KeywordRetrievalService()

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        candidate_k: int = 10,
    ) -> list[dict]:

        vector_results = self.vector_service.search(
            db=db,
            query=query,
            top_k=candidate_k,
        )

        keyword_results = self.keyword_service.search(
            db=db,
            query=query,
            top_k=candidate_k,
        )

        k = 60
        fused = {}

        for rank, result in enumerate(vector_results, start=1):
            chunk_id = result["chunk_id"]

            fused.setdefault(
                chunk_id,
                {
                    **result,
                    "vector_rank": None,
                    "keyword_rank": None,
                    "rrf_score": 0.0,
                },
            )

            fused[chunk_id]["vector_rank"] = rank
            fused[chunk_id]["rrf_score"] += 1 / (k + rank)

        for rank, result in enumerate(keyword_results, start=1):
            chunk_id = result["chunk_id"]

            if chunk_id not in fused:
                fused[chunk_id] = {
                    **result,
                    "vector_rank": None,
                    "keyword_rank": rank,
                    "rrf_score": 0.0,
                }
            else:
                fused[chunk_id]["keyword_rank"] = rank

            fused[chunk_id]["rrf_score"] += 1 / (k + rank)

        results = sorted(
            fused.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        return results[:top_k]
