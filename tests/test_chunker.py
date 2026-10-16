
import pytest

from app.ingestion.chunker import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_short_text_returns_one_chunk():
    text = "Annual leave policy for employees."

    assert chunk_text(text) == [text]


def test_long_text_is_split_into_chunks():
    text = "A" * 2500

    chunks = chunk_text(text, chunk_size=1000, overlap=150)

    assert len(chunks) == 3
    assert all(len(chunk) <= 1000 for chunk in chunks)
    assert chunks[0][-150:] == chunks[1][:150]
    assert chunks[1][-150:] == chunks[2][:150]


def test_invalid_chunk_size_raises_error():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("Example", chunk_size=0)


def test_invalid_overlap_raises_error():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("Example", chunk_size=100, overlap=100)
