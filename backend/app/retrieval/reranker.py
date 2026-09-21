from pathlib import Path

from sentence_transformers import CrossEncoder


MODEL_NAME = "BAAI/bge-reranker-base"

LOCAL_MODEL_PATH = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--BAAI--bge-reranker-base"
    / "snapshots"
)


class RerankerService:
    def __init__(self):
        local_snapshots = list(
            LOCAL_MODEL_PATH.glob("*")
        ) if LOCAL_MODEL_PATH.exists() else []

        if local_snapshots:
            model_path = str(local_snapshots[0])
            print(
                f"Loading local reranker model: {model_path}"
            )
        else:
            model_path = MODEL_NAME
            print(
                f"Loading reranker model from Hugging Face: "
                f"{MODEL_NAME}"
            )

        self.model = CrossEncoder(model_path)

        print("Reranker model loaded.")

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if not results:
            return []

        pairs = [
            [query, result["content"]]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):
            item = dict(result)
            item["reranker_score"] = float(score)
            reranked.append(item)

        reranked.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        return reranked[:top_k]
