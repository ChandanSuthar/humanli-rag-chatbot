import chromadb
from chromadb.config import Settings
from typing import List


class ChromaVectorStore:
    def __init__(self, persist_directory: str):
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False
            )
        )
        self.collection = self.client.get_or_create_collection(
            name="website_content"
        )

    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
        ids: List[str]
    ):
        """
        Stores documents with embeddings and metadata.
        """
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        # Persistence is automatic in newer Chroma versions

    def query(self, query_embedding: List[float], n_results: int = 4):
        """
        Queries the vector database for similar documents.
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
