
from unittest.mock import Mock

import pytest

from app.retrieval.vector_store import VectorStore


@pytest.fixture
def store():
    vector_store = VectorStore()
    vector_store.embedding_service = Mock()

    # Simple normalized vectors for deterministic retrieval testing.
    vector_store.embedding_service.embed_texts.return_value = [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.8, 0.6],
    ]

    vector_store.embedding_service.embed_query.return_value = [
        [0.0, 1.0]
    ]

    return vector_store


def test_build_and_retrieve_relevant_chunk(store):
    chunks = [
        "Employees receive 20 annual leave days.",
        "The office internet password changes monthly.",
        "Annual leave requests require manager approval.",
    ]

    store.build(chunks)

    results = store.search("How do I request annual leave?", top_k=2)

    assert results[0] == chunks[1]
    assert len(results) == 2


def test_search_before_build_raises_error():
    vector_store = VectorStore()

    with pytest.raises(RuntimeError, match="Build the vector index"):
        vector_store.search("What is the leave policy?")


def test_empty_chunks_are_rejected():
    vector_store = VectorStore()

    with pytest.raises(ValueError, match="no chunks"):
        vector_store.build([])
