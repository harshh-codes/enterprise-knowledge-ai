
from google import genai

from app.core.config import settings


MODEL_NAME = "gemini-3.5-flash-lite"


class GeminiService:
    """Generate responses using the Gemini API."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Check your .env configuration."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_answer(self, prompt: str) -> str:
        """Generate an answer from a supplied prompt."""

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        answer = response.text

        if not answer or not answer.strip():
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return answer.strip()
