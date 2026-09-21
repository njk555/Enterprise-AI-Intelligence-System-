from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enterprise import Document, DocumentChunk
from app.embeddings.service import EmbeddingService


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = self.embedding_service.embed_text(query)

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        results = (
            db.execute(
                select(
                    DocumentChunk.id,
                    DocumentChunk.document_id,
                    DocumentChunk.chunk_index,
                    DocumentChunk.content,
                    Document.title,
                    distance.label("distance"),
                )
                .join(
                    Document,
                    Document.id == DocumentChunk.document_id,
                )
                .where(
                    DocumentChunk.embedding.is_not(None)
                )
                .order_by(distance)
                .limit(top_k)
            )
            .mappings()
            .all()
        )

        return [
            {
                "chunk_id": row["id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "document_title": row["title"],
                "content": row["content"],
                "distance": float(row["distance"]),
            }
            for row in results
        ]