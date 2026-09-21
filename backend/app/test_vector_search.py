from sqlalchemy import text

from app.core.database import engine
from app.embeddings.service import EmbeddingService


def main():
    embedding_service = EmbeddingService()

    query = "Why did enterprise revenue decline during Q4?"

    query_embedding = embedding_service.embed_text(query)

    vector_string = "[" + ",".join(
        str(value) for value in query_embedding
    ) + "]"

    with engine.connect() as connection:
        results = connection.execute(
            text("""
                SELECT
                    dc.id,
                    dc.document_id,
                    dc.chunk_index,
                    LEFT(dc.content, 120) AS content_preview,
                    dc.embedding <=> CAST(:embedding AS vector) AS distance
                FROM document_chunks dc
                WHERE dc.embedding IS NOT NULL
                ORDER BY dc.embedding <=> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {
                "embedding": vector_string
            },
        ).fetchall()

    print("\nVector search results:\n")

    for row in results:
        print(f"Chunk ID: {row.id}")
        print(f"Document ID: {row.document_id}")
        print(f"Chunk index: {row.chunk_index}")
        print(f"Distance: {row.distance:.6f}")
        print(f"Preview: {row.content_preview}")
        print("-" * 60)


if __name__ == "__main__":
    main()