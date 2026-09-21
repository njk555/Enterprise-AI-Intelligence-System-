from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.enterprise import Document, DocumentChunk


def main():
    db = SessionLocal()

    try:
        document = db.scalar(
            select(Document)
            .order_by(Document.id.desc())
        )

        if not document:
            print("Document not found.")
            return

        chunks = db.scalars(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document.id)
            .order_by(DocumentChunk.chunk_index)
        ).all()

        print(f"Document: {document.title}")
        print(f"Total chunks: {len(chunks)}")

        for chunk in chunks:
            print("\n" + "=" * 70)
            print(f"CHUNK {chunk.chunk_index}")
            print("=" * 70)
            print(chunk.content)

    finally:
        db.close()


if __name__ == "__main__":
    main()