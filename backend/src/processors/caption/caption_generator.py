"""
BLIP image caption generator for MVRAG AI.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import Image
from transformers import (
    BlipForConditionalGeneration,
    BlipProcessor,
)

from src.config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_blip_components():

    logger.info(
        "Loading BLIP model: %s",
        settings.IMAGE_CAPTION_MODEL,
    )

    processor = (
        BlipProcessor.from_pretrained(
            settings.IMAGE_CAPTION_MODEL
        )
    )

    model = (
        BlipForConditionalGeneration.from_pretrained(
            settings.IMAGE_CAPTION_MODEL
        )
    )

    logger.info(
        "BLIP model loaded successfully."
    )

    return processor, model


class CaptionGenerator:
    """
    Generates captions for video frames.
    """

    def __init__(self):

        (
            self.processor,
            self.model,
        ) = get_blip_components()

    def generate_caption(
        self,
        image_path: str | Path,
    ) -> str:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                image_path
            )

        image = (
            Image.open(image_path)
            .convert("RGB")
        )

        inputs = self.processor(
            image,
            return_tensors="pt",
        )

        output = self.model.generate(
            **inputs,
            max_new_tokens=30,
        )

        return self.processor.decode(
            output[0],
            skip_special_tokens=True,
        )