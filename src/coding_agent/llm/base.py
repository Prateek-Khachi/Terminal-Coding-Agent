from abc import ABC, abstractmethod

from coding_agent.llm.types import LLMResponse, Message


class LLMProvider(ABC):
    """Abstract interface for an LLM provider."""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        """Generate a response from the language model."""
        raise NotImplementedError
    