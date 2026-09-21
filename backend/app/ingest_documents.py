from pathlib import Path

from app.core.database import SessionLocal
from app.ingestion.pipeline import ingest_text_document


DOCUMENTS_DIR = Path("data/documents")


def main():
    db = SessionLocal()

    try:
        files = sorted(DOCUMENTS_DIR.glob("*.txt"))

        if not files:
            print("No text documents found.")
            return

        print(f"Found {len(files)} document(s).")

        for file_path in files:
            title = file_path.stem.replace("_", " ").title()

            print("\n" + "=" * 70)
            print(f"Ingesting: {file_path.name}")

            document = ingest_text_document(
                db=db,
                file_path=str(file_path),
                title=title,
            )

            print(f"Document ID: {document.id}")
            print(f"Title: {document.title}")
            print(f"Chunks: {len(document.chunks)}")

        print("\nAll documents ingested successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
