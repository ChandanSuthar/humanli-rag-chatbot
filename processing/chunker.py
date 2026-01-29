from typing import List
import tiktoken

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


class TextChunker:
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def chunk_text(self, text: str) -> List[str]:
        """
        Splits text into overlapping token-based chunks.
        """

        if not text or not text.strip():
            return []

        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)

            start = end - self.overlap
            if start < 0:
                start = 0

        return chunks
