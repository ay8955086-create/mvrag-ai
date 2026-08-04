"""
LLM service.
"""

from __future__ import annotations

from src.core.logger import get_logger

from src.llm.gemini_client import GeminiClient
from src.llm.prompt_builder import PromptBuilder

logger = get_logger(__name__)


class LLMService:

    def __init__(self):

        self.client = GeminiClient()

    def answer(
        self,
        question: str,
        context: list[dict],
    ) -> str:

        prompt = PromptBuilder.build(
            question,
            context,
        )

        logger.info("Sending prompt to Gemini.")

        return self.client.generate(prompt)