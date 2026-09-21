import os

from dotenv import load_dotenv
from groq import Groq

from app.llm.service import LLMService


load_dotenv()


class GroqLLMService(LLMService):
    """
    LLM service implementation using Groq.
    """

    MODEL_NAME = "openai/gpt-oss-20b"

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=messages,
            temperature=0.1,
        )

        return response.choices[0].message.content
