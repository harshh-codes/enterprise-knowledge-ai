
import fitz

from app.ingestion.pipeline import process_pdf


def test_process_pdf_extracts_and_chunks_text(tmp_path):
    pdf_path = tmp_path / "sample_policy.pdf"

    policy_text = (
        "Annual leave policy. "
        "Employees may request annual leave through their manager. "
    ) * 30

    with fitz.open() as document:
        page = document.new_page()
        page.insert_textbox(
            fitz.Rect(50, 50, 550, 750),
            policy_text,
            fontsize=10,
        )
        document.save(pdf_path)

    chunks = process_pdf(
        pdf_path,
        chunk_size=200,
        overlap=30,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 200 for chunk in chunks)
    assert all("[Page 1]" in chunks[0] for _ in [0])
    assert any("Annual leave policy" in chunk for chunk in chunks)
