
from unittest.mock import Mock, patch

import pytest

from app.retrieval.retriever import DocumentRetriever


def test_index_directory_processes_pdfs(tmp_path):
    pdf_file = tmp_path / "sample_hr_policy.pdf"
    pdf_file.touch()

    with patch(
        "app.retrieval.retriever.process_pdf",
        return_value=[
            "[Page 1]\nEmployees receive 20 annual leave days."
        ],
    ), patch(
        "app.retrieval.retriever.VectorStore"
    ) as mock_store_class:
        retriever = DocumentRetriever()

        chunk_count = retriever.index_directory(tmp_path)

        assert chunk_count == 1
        assert retriever.document_count == 1

        indexed_chunks = (
            mock_store_class.return_value.build.call_args.args[0]
        )
        assert "sample_hr_policy.pdf" in indexed_chunks[0]
        assert "20 annual leave days" in indexed_chunks[0]


def test_index_directory_rejects_missing_directory(tmp_path):
    retriever = DocumentRetriever()

    with pytest.raises(NotADirectoryError):
        retriever.index_directory(tmp_path / "missing")


def test_index_directory_rejects_empty_directory(tmp_path):
    retriever = DocumentRetriever()

    with pytest.raises(ValueError, match="No PDF files found"):
        retriever.index_directory(tmp_path)


def test_search_delegates_to_vector_store():
    retriever = DocumentRetriever()
    retriever.vector_store = Mock()
    retriever.vector_store.search.return_value = [
        "[Page 1] Sample policy"
    ]

    results = retriever.search("What is the policy?", top_k=2)

    assert results == ["[Page 1] Sample policy"]
    retriever.vector_store.search.assert_called_once_with(
        query="What is the policy?",
        top_k=2,
    )
