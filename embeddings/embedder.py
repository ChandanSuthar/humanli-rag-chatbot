from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of text chunks.
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )

        return embeddings.tolist()
