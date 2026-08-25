"""
OCR processor for MVRAG AI.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import easyocr

from src.core.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_ocr_reader():

    logger.info(
        "Loading EasyOCR model..."
    )

    reader = easyocr.Reader(
        ["en"],
    )

    logger.info(
        "EasyOCR model loaded."
    )

    return reader


class OCRProcessor:
    """
    Performs OCR on extracted video frames.
    """

    def __init__(self):

        self.reader = get_ocr_reader()

    def extract_text(
        self,
        image_path: str | Path,
    ) -> dict:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                image_path
            )

        result = self.reader.readtext(
            str(image_path)
        )

        extracted_text = []
        confidences = []

        for _, text, confidence in result:

            extracted_text.append(text)

            confidences.append(
                confidence
            )

        return {
            "text": "\n".join(
                extracted_text
            ),
            "confidence": (
                sum(confidences)
                / len(confidences)
                if confidences
                else 0.0
            ),
            "raw": result,
        }