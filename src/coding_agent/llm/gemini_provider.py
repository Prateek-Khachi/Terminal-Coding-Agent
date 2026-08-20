from google import genai

from coding_agent.config import get_settings
from coding_agent.llm.base import LLMProvider
from coding_agent.llm.types import LLMResponse, Message


class GeminiProvider(LLMProvider):
    """LLM provider implementation using Google Gemini."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.gemini_api_key:
            raise ValueError(
                "Gemini API key is not configured. "
                "Set GEMINI_API_KEY in your .env file."
            )

        self.model = settings.model
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    def generate(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        contents = "\n".join(
            f"{message.role}: {message.content}"
            for message in messages
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )

        return LLMResponse(
            content=response.text,
            model=self.model,
        )