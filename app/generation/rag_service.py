
from app.generation.gemini_service import GeminiService
from app.generation.prompt_builder import build_rag_prompt


class RAGService:
    """Generate answers grounded in retrieved evidence."""

    def __init__(self) -> None:
        self.gemini = GeminiService()

    def answer_question(
        self,
        question: str,
        context_chunks: list[str],
    ) -> str:
        prompt = build_rag_prompt(
            question=question,
            context_chunks=context_chunks,
        )

        return self.gemini.generate_answer(prompt)
