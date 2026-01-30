from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from src.config import Config

class TextProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        # Load local embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)

    def chunk_text(self, text):
        return self.text_splitter.split_text(text)

    def get_embeddings(self, chunks):
        # Determine strict list for ChromaDB
        embeddings = self.embedding_model.encode(chunks)
        return embeddings.tolist()