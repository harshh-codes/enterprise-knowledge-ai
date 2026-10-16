
from pathlib import Path

import fitz


def extract_text(pdf_path: str | Path) -> str:
    """Extract text from a PDF file."""

    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The supplied file must be a PDF.")

    pages = []

    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(f"[Page {page_number}]\n{text}")

    extracted_text = "\n\n".join(pages)

    if not extracted_text:
        raise ValueError(
            "No extractable text found. The PDF may be empty "
            "or scanned and require OCR."
        )

    return extracted_text
