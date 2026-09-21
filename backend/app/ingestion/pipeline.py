from pathlib import Path

from sqlalchemy.orm import Session

from app.models.enterprise import Document, DocumentChunk
from app.ingestion.loader import load_text_file
from app.ingestion.chunker import chunk_text


def ingest_text_document(
    db: Session,
    file_path: str,
    title: str,
) -> Document:
    text = load_text_file(file_path)
    chunks = chunk_text(text)

    document = Document(
        title=title,
        source_type="text",
        source_path=str(Path(file_path)),
        description="Enterprise business document",
    )

    db.add(document)
    db.flush()

    for index, chunk_data in enumerate(chunks):
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk_data["content"],
            metadata_json=chunk_data["section"],
        )

        db.add(chunk)

    db.commit()
    db.refresh(document)

    return document
