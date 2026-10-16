
import fitz
import pytest

from app.ingestion.pdf_loader import extract_text


def test_extract_text_from_pdf(tmp_path):
    pdf_path = tmp_path / "sample_policy.pdf"

    with fitz.open() as document:
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Annual leave policy: Employees receive annual leave.",
        )
        document.save(pdf_path)

    result = extract_text(pdf_path)

    assert "[Page 1]" in result
    assert "Annual leave policy" in result
    assert "Employees receive annual leave." in result


def test_missing_pdf_raises_error(tmp_path):
    missing_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text(missing_path)


def test_non_pdf_file_raises_error(tmp_path):
    text_path = tmp_path / "notes.txt"
    text_path.write_text("This is not a PDF.", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a PDF"):
        extract_text(text_path)


def test_pdf_without_extractable_text_raises_error(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    with fitz.open() as document:
        document.new_page()
        document.save(pdf_path)

    with pytest.raises(ValueError, match="No extractable text"):
        extract_text(pdf_path)
