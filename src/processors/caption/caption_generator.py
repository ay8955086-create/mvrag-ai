"""
BLIP image caption generator for MVRAG AI.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from transformers import (
    BlipForConditionalGeneration,
    BlipProcessor,
)

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class CaptionGenerator:
    """
    Generates captions for video frames using BLIP.
    """

    def __init__(self):

        logger.info(
            "Loading BLIP model: %s",
            settings.IMAGE_CAPTION_MODEL,
        )

        self.processor = BlipProcessor.from_pretrained(
            settings.IMAGE_CAPTION_MODEL
        )

        self.model = BlipForConditionalGeneration.from_pretrained(
            settings.IMAGE_CAPTION_MODEL
        )

    def generate_caption(self, image_path: str | Path) -> str:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            image,
            return_tensors="pt",
        )

        output = self.model.generate(
            **inputs,
            max_new_tokens=30,
        )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True,
        )

        logger.info(
            "Caption generated for %s",
            image_path.name,
        )

        return caption