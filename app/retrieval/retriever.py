
from pathlib import Path
import re

from app.ingestion.pipeline import process_pdf
from app.retrieval.vector_store import VectorStore


class DocumentRetriever:
    """Process PDF documents and retrieve passages with source metadata."""

    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.document_count = 0

    def index_directory(self, directory: str | Path) -> int:
        """Index PDF files and preserve their filenames and page markers."""
        directory_path = Path(directory)

        if not directory_path.is_dir():
            raise NotADirectoryError(
                f"Directory not found: {directory_path}"
            )

        pdf_files = sorted(directory_path.glob("*.pdf"))

        if not pdf_files:
            raise ValueError(
                f"No PDF files found in {directory_path}"
            )

        all_chunks: list[str] = []

        for pdf_path in pdf_files:
            chunks = process_pdf(pdf_path)

            for chunk in chunks:
                page_match = re.search(
                    r"\[Page\s+(\d+)\]",
                    chunk,
                )
                page_number = (
                    page_match.group(1) if page_match else "Unknown"
                )

                all_chunks.append(
                    f"[Source: {pdf_path.name}]\n"
                    f"[Page: {page_number}]\n"
                    f"{chunk}"
                )

        self.vector_store.build(all_chunks)
        self.document_count = len(pdf_files)

        return len(all_chunks)

    def search(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[str]:
        """Retrieve relevant passages with source metadata."""
        return self.vector_store.search(
            query=question,
            top_k=top_k,
        )
