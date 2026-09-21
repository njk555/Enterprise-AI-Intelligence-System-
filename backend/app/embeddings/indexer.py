from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.enterprise import DocumentChunk
from app.embeddings.service import EmbeddingService


def index_embeddings(batch_size: int = 32):
    db = SessionLocal()

    try:
        chunks = db.scalars(
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
            .order_by(DocumentChunk.id)
        ).all()

        if not chunks:
            print("No chunks need embeddings.")
            return

        print(f"Found {len(chunks)} chunk(s) without embeddings.")

        embedding_service = EmbeddingService()

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]

            texts = [
                chunk.content
                for chunk in batch
            ]

            embeddings = embedding_service.embed_documents(
                texts
            )

            for chunk, embedding in zip(
                batch,
                embeddings,
            ):
                chunk.embedding = embedding

            db.commit()

            print(
                f"Embedded {min(start + batch_size, len(chunks))}"
                f"/{len(chunks)} chunk(s)."
            )

        print("Embedding indexing completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    index_embeddings()