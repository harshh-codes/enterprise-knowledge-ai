
from pathlib import Path

import pymupdf


def extract_pages(pdf_path: str | Path) -> list[tuple[int, str]]:
    """Extract non-empty text from a PDF, preserving page numbers."""
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The supplied file must be a PDF.")

    pages: list[tuple[int, str]] = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append((page_number, text))

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be empty "
            "or scanned and require OCR."
        )

    return pages


def extract_text(pdf_path: str | Path) -> str:
    """Extract PDF text while retaining page markers."""
    pages = extract_pages(pdf_path)

    return "\n\n".join(
        f"[Page {page_number}]\n{text}"
        for page_number, text in pages
    )
