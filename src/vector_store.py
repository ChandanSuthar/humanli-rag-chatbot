import chromadb
from chromadb.config import Settings
from src.config import Config
import uuid

class VectorStore:
    def __init__(self):
        # Using EphemeralClient for session-based storage (good for demos)
        # For production, use PersistentClient(path=Config.CHROMA_PATH)
        self.client = chromadb.EphemeralClient()
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks, embeddings):
        if not chunks:
            return
            
        ids = [str(uuid.uuid4()) for _ in chunks]
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    def query(self, query_embedding, n_results=3):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        # Flatten the list of documents
        if results and results['documents']:
            return results['documents'][0]
        return []
        
    def clear(self):
        self.client.delete_collection(Config.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(name=Config.COLLECTION_NAME)