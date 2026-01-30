from typing import List
import numpy as np

from config.settings import TOP_K_RESULTS, SIMILARITY_THRESHOLD
from embeddings.embedder import EmbeddingGenerator
from vectorstore.chroma_store import ChromaVectorStore

FALLBACK_RESPONSE = "The answer is not available on the provided website."


class Retriever:
    def __init__(self, vector_db_path: str):
        self.embedder = EmbeddingGenerator()
        self.store = ChromaVectorStore(vector_db_path)

    def retrieve(self, question: str) -> dict:
        """
        Retrieves relevant website content for a user question.
        """

        if not question or not question.strip():
            return {
                "answer": FALLBACK_RESPONSE,
                "contexts": []
            }

        # Embed the question
        question_embedding = self.embedder.generate([question])[0]

        # Query vector DB
        results = self.store.query(
            query_embedding=question_embedding,
            n_results=TOP_K_RESULTS
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents or not distances:
            return {
                "answer": FALLBACK_RESPONSE,
                "contexts": []
            }

        # Convert distances to similarity scores
        similarities = [1 - d for d in distances]

        # Filter by similarity threshold
        filtered_contexts = [
            doc for doc, score in zip(documents, similarities)
            if score >= SIMILARITY_THRESHOLD
        ]

        if not filtered_contexts:
            return {
                "answer": FALLBACK_RESPONSE,
                "contexts": []
            }

        # Return retrieved contexts (generation comes later)
        return {
            "answer": None,
            "contexts": filtered_contexts
        }
