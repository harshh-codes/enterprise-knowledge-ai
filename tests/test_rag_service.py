
from unittest.mock import Mock, patch

import pytest

from app.generation.rag_service import RAGService


def test_answer_question_uses_retrieved_evidence():
    with patch(
        "app.generation.rag_service.GeminiService"
    ) as mock_gemini:
        mock_gemini.return_value.generate_answer.return_value = (
            "Employees receive 20 annual leave days. [Evidence 1]"
        )

        service = RAGService()
        answer = service.answer_question(
            "How many annual leave days do employees receive?",
            ["[Page 2] Employees receive 20 annual leave days."],
        )

        assert "20 annual leave days" in answer
        assert "[Evidence 1]" in answer

        prompt = mock_gemini.return_value.generate_answer.call_args.args[0]
        assert "Employees receive 20 annual leave days" in prompt


def test_answer_question_rejects_empty_question():
    with patch("app.generation.rag_service.GeminiService"):
        service = RAGService()

        with pytest.raises(ValueError, match="Question cannot be empty"):
            service.answer_question("", ["Sample policy evidence"])


def test_answer_question_rejects_missing_evidence():
    with patch("app.generation.rag_service.GeminiService"):
        service = RAGService()

        with pytest.raises(ValueError, match="context chunk"):
            service.answer_question("What is the leave policy?", [])
