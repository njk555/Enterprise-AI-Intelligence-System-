from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.enterprise import DocumentChunk
from app.embeddings.service import EmbeddingService


def main():
    db = SessionLocal()

    try:
        chunk = db.scalar(
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
            .order_by(DocumentChunk.id)
        )

        if chunk is None:
            print("No chunk without an embedding was found.")
            return

        print(f"Embedding chunk ID: {chunk.id}")
        print(f"Text preview: {chunk.content[:100]}...")

        embedding_service = EmbeddingService()

        embedding = embedding_service.embed_text(
            chunk.content
        )

        print(f"Generated dimensions: {len(embedding)}")

        chunk.embedding = embedding

        db.commit()

        print("Embedding stored successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()