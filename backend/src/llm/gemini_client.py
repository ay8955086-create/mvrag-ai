"""
Gemini client for MVRAG AI.
"""

from __future__ import annotations

from google import genai

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """
    Wrapper around Google's Gemini API.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        logger.info(
            "Gemini client initialized using model: %s",
            settings.LLM_MODEL,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from Gemini.
        """

        response = self.client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=prompt,
        )

        return response.text.strip()