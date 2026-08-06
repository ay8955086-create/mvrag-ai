"""
Semantic chunk generator for MVRAG AI.

Combines Whisper transcript, OCR text, and BLIP captions
into multimodal chunks ready for embedding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ChunkData:
    """
    Represents one semantic chunk.
    """

    chunk_index: int
    start_time: float
    end_time: float

    transcript: str
    ocr_text: str
    caption: str

    combined_text: str


class ChunkGenerator:
    """
    Creates multimodal chunks.
    """

    def generate_chunks(
        self,
        transcript_segments: list[dict[str, Any]],
        ocr_results: list[dict[str, Any]],
        captions: list[dict[str, Any]],
    ) -> list[ChunkData]:
        """
        Merge transcript, OCR and captions.
        """

        logger.info("Generating semantic chunks...")

        chunks: list[ChunkData] = []

        for index, segment in enumerate(transcript_segments):

            start = segment["start"]
            end = segment["end"]

            transcript = segment["text"].strip()

            ocr_text = self._collect_ocr(
                start,
                end,
                ocr_results,
            )

            caption = self._collect_caption(
                start,
                end,
                captions,
            )

            combined = self._combine(
                transcript,
                ocr_text,
                caption,
            )

            chunks.append(
                ChunkData(
                    chunk_index=index,
                    start_time=start,
                    end_time=end,
                    transcript=transcript,
                    ocr_text=ocr_text,
                    caption=caption,
                    combined_text=combined,
                )
            )

        logger.info("Generated %d chunks.", len(chunks))

        return chunks

    def _collect_ocr(
        self,
        start: float,
        end: float,
        ocr_results: list[dict[str, Any]],
    ) -> str:

        texts = [
            item["text"]
            for item in ocr_results
            if start <= item["timestamp"] <= end
        ]

        return "\n".join(texts)

    def _collect_caption(
        self,
        start: float,
        end: float,
        captions: list[dict[str, Any]],
    ) -> str:

        texts = [
            item["caption"]
            for item in captions
            if start <= item["timestamp"] <= end
        ]

        return "\n".join(texts)

    def _combine(
        self,
        transcript: str,
        ocr: str,
        caption: str,
    ) -> str:

        return (
            f"Transcript:\n{transcript}\n\n"
            f"OCR:\n{ocr}\n\n"
            f"Caption:\n{caption}"
        )