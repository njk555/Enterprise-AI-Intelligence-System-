from sqlalchemy import delete

from app.core.database import SessionLocal
from app.models.enterprise import Document, DocumentChunk


def main():
    db = SessionLocal()

    try:
        # Delete chunks first because they reference documents.
        chunks_deleted = db.execute(
            delete(DocumentChunk)
        ).rowcount

        # Now the parent documents can safely be deleted.
        documents_deleted = db.execute(
            delete(Document)
        ).rowcount

        db.commit()

        print(f"Deleted {chunks_deleted} document chunk(s).")
        print(f"Deleted {documents_deleted} document(s).")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()