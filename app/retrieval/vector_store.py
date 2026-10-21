
from pathlib import Path

import faiss
import numpy as np

from app.retrieval.embeddings import EmbeddingService


class VectorStore:
    """Store document embeddings and retrieve relevant text chunks."""

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.index = None
        self.chunks: list[str] = []

    def build(self, chunks: list[str]) -> None:
        if not chunks:
            raise ValueError("Cannot build an index with no chunks.")

        if any(not chunk.strip() for chunk in chunks):
            raise ValueError("Chunks must not contain empty strings.")

        vectors = self.embedding_service.embed_texts(chunks)
        vectors = np.asarray(vectors, dtype=np.float32)

        dimension = vectors.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(vectors)

        self.index = index
        self.chunks = list(chunks)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        if self.index is None:
            raise RuntimeError("Build the vector index before searching.")

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query_vector = self.embedding_service.embed_query(query)
        query_vector = np.asarray(query_vector, dtype=np.float32)

        count = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_vector, count)

        return [
            self.chunks[int(i)]
            for i in indices[0]
            if i >= 0
        ]
