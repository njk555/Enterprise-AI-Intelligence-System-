from sqlalchemy import text
from sqlalchemy.orm import Session


class KeywordRetrievalService:

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        sql = text("""
            SELECT
                dc.id AS chunk_id,
                dc.document_id,
                dc.chunk_index,
                dc.content,
                d.title AS document_title,
                ts_rank_cd(
                    to_tsvector('english', dc.content),
                    websearch_to_tsquery('english', :query)
                ) AS score
            FROM document_chunks dc
            JOIN documents d
                ON d.id = dc.document_id
            WHERE
                websearch_to_tsquery('english', :query)
                @@ to_tsvector('english', dc.content)
            ORDER BY score DESC
            LIMIT :top_k
        """)

        results = db.execute(
            sql,
            {
                "query": query,
                "top_k": top_k,
            },
        ).mappings().all()

        return [
            {
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "document_title": row["document_title"],
                "content": row["content"],
                "score": float(row["score"]),
            }
            for row in results
        ]
