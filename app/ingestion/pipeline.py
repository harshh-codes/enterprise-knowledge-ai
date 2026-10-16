
from pathlib import Path

from app.ingestion.chunker import chunk_text
from app.ingestion.pdf_loader import extract_text


def process_pdf(
    pdf_path: str | Path,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Extract text from a PDF and split it into chunks."""

    extracted_text = extract_text(pdf_path)

    chunks = chunk_text(
        extracted_text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    if not chunks:
        raise ValueError("PDF processing produced no text chunks.")

    return chunks
