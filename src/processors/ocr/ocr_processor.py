"""
OCR processor for MVRAG AI.

Extracts text from video frames using EasyOCR.
"""

from __future__ import annotations

from pathlib import Path

import easyocr

from src.core.logger import get_logger

logger = get_logger(__name__)


class OCRProcessor:
    """
    Performs OCR on extracted video frames.
    """

    def __init__(self, languages: list[str] | None = None):
        if languages is None:
            languages = ["en"]

        logger.info("Loading EasyOCR model...")
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_path: str | Path) -> dict:
        """
        Extract text from an image.

        Parameters
        ----------
        image_path : str | Path

        Returns
        -------
        dict
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        logger.info("Running OCR on %s", image_path.name)

        result = self.reader.readtext(str(image_path))

        extracted_text = []
        confidences = []

        for _, text, confidence in result:
            extracted_text.append(text)
            confidences.append(confidence)

        return {
            "text": "\n".join(extracted_text),
            "confidence": (
                sum(confidences) / len(confidences)
                if confidences
                else 0.0
            ),
            "raw": result,
        }