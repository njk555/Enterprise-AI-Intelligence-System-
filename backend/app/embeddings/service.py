from pathlib import Path

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"

LOCAL_MODEL_PATH = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--BAAI--bge-small-en-v1.5"
    / "snapshots"
    / "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
)


class EmbeddingService:
    def __init__(self):
        if LOCAL_MODEL_PATH.exists():
            model_path = str(LOCAL_MODEL_PATH)
            print(f"Loading local embedding model: {model_path}")
        else:
            model_path = MODEL_NAME
            print(f"Loading embedding model from Hugging Face: {MODEL_NAME}")

        self.model = SentenceTransformer(model_path)

        print("Embedding model loaded.")

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Cannot embed empty text.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
