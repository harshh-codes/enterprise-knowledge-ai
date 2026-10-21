
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """Generate vector embeddings for text."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_texts(self, texts: list[str]):
        """Convert multiple texts into normalized embeddings."""

        if not texts:
            raise ValueError("texts must not be empty.")

        if any(not text.strip() for text in texts):
            raise ValueError("texts must not contain empty strings.")

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

    def embed_query(self, query: str):
        """Convert a single query into a normalized embedding."""

        if not query.strip():
            raise ValueError("query must not be empty.")

        return self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
