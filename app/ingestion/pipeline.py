
from pathlib import Path

from app.ingestion.chunker import chunk_text
from app.ingestion.pdf_loader import extract_pages


def process_pdf(
    pdf_path: str | Path,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Chunk each PDF page while preserving accurate page numbers."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    pages = extract_pages(pdf_path)
    all_chunks: list[str] = []

    for page_number, page_text in pages:
        page_marker = f"[Page {page_number}]\n"
        content_size = chunk_size - len(page_marker)

        if content_size <= overlap:
            raise ValueError(
                "chunk_size is too small for the page marker and overlap."
            )

        page_chunks = chunk_text(
            page_text,
            chunk_size=content_size,
            overlap=overlap,
        )

        for chunk in page_chunks:
            all_chunks.append(f"{page_marker}{chunk}")

    if not all_chunks:
        raise ValueError("PDF processing produced no text chunks.")

    return all_chunks
