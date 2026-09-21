from app.embeddings.service import EmbeddingService


def main():
    service = EmbeddingService()

    text = "Why did enterprise revenue decline during Q4?"

    embedding = service.embed_text(text)

    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")


if __name__ == "__main__":
    main()