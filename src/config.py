import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Settings
    # gemini-1.5-flash is currently the fastest and most cost-effective for RAG
    # Try this if 'gemini-1.5-flash' fails:
    GEMINI_MODEL_NAME = "gemini-flash-latest"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    
    # Chunking Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Vector Store Settings
    CHROMA_PATH = "chroma_db"
    COLLECTION_NAME = "website_content"
    
    # Crawler Settings
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"