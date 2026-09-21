from abc import ABC, abstractmethod


class LLMService(ABC):
    """
    Abstract interface for an LLM provider.

    The RAG pipeline will depend on this interface rather
    than directly depending on a specific LLM provider.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """
        Generate a response from the LLM.
        """
        raise NotImplementedError
