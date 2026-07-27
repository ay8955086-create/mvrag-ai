"""
Main processing pipeline for MVRAG AI.

This module orchestrates the complete video processing workflow.
"""

from __future__ import annotations

from pathlib import Path

from src.core.logger import get_logger
from src.utils.video_metadata import extract_video_metadata

from src.processors.audio.audio_extractor import AudioExtractor
from src.processors.whisper.transcriber import WhisperTranscriber
from src.processors.frames.frame_extractor import FrameExtractor
from src.processors.ocr.ocr_processor import OCRProcessor
from src.processors.caption.caption_generator import CaptionGenerator
logger = get_logger(__name__)


class VideoPipeline:
    """
    Executes the complete AI pipeline for one uploaded video.
    """

    def __init__(self):
        """
        Initialize all pipeline components.
        """

        self.audio_extractor = AudioExtractor()
        self.whisper = WhisperTranscriber()
        self.frame_extractor = FrameExtractor()
        self.ocr_processor = OCRProcessor()
        self.caption_generator = CaptionGenerator()

        logger.info("VideoPipeline initialized.")

    # ==========================================================
    # Main Pipeline
    # ==========================================================

    def process(
        self,
        video_path: str | Path,
    ) -> dict:
        """
        Execute the complete processing pipeline.
        """

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(video_path)

        logger.info("=" * 60)
        logger.info("Processing video: %s", video_path.name)

        # ------------------------------------------------------
        # Step 1 : Metadata
        # ------------------------------------------------------

        metadata = self.extract_metadata(video_path)

        # ------------------------------------------------------
        # Step 2 : Audio Extraction
        # ------------------------------------------------------

        audio_path = self.extract_audio(video_path)

        # ------------------------------------------------------
        # Step 3 : Whisper Transcription
        # ------------------------------------------------------

        transcript = self.transcribe(audio_path)

        # ------------------------------------------------------
        # Step 4 : Frame Extraction
        # ------------------------------------------------------

        frames = self.extract_frames(video_path)

        # ------------------------------------------------------
        # Step 5 : OCR
        # ------------------------------------------------------

        ocr_results = self.extract_ocr(frames)

        # ------------------------------------------------------
        # Step 6 : BLIP Caption Generation
        # ------------------------------------------------------

        captions = self.generate_captions(frames)

        logger.info("=" * 60)
        logger.info("Video processing completed successfully.")

        return {
            "metadata": metadata,
            "audio_path": audio_path,
            "transcript": transcript,
            "frames": frames,
            "ocr": ocr_results,
            "captions": captions,
        }

    # ==========================================================
    # Metadata Extraction
    # ==========================================================

    def extract_metadata(
        self,
        video_path: Path,
    ) -> dict:
        """
        Extract metadata from the uploaded video.
        """

        logger.info("Metadata extraction started.")

        metadata = extract_video_metadata(str(video_path))

        logger.info("Metadata extracted successfully.")

        logger.info(
            "Duration : %.2f sec | FPS : %.2f | Resolution : %dx%d | Size : %.2f MB",
            metadata["duration"],
            metadata["fps"],
            metadata["width"],
            metadata["height"],
            metadata["size_mb"],
        )

        return metadata

    # ==========================================================
    # Audio Extraction
    # ==========================================================

    def extract_audio(
        self,
        video_path: Path,
    ) -> Path:
        """
        Extract audio from the uploaded video.
        """

        logger.info("Audio extraction started.")

        audio_path = self.audio_extractor.extract(video_path)

        logger.info("Audio extraction completed.")

        logger.info("Audio saved at : %s", audio_path)

        return audio_path

    # ==========================================================
    # Whisper Transcription
    # ==========================================================

    def transcribe(
        self,
        audio_path: Path,
    ) -> dict:
        """
        Transcribe extracted audio using Whisper.
        """

        logger.info("Whisper transcription started.")

        result = self.whisper.transcribe(audio_path)

        logger.info("Whisper transcription completed.")

        logger.info(
            "Detected Language : %s",
            result.get("language", "unknown"),
        )

        logger.info(
            "Transcript Segments : %d",
            len(result.get("segments", [])),
        )

        return result

    # ==========================================================
    # Frame Extraction
    # ==========================================================

    def extract_frames(
        self,
        video_path: Path,
    ) -> list[Path]:
        """
        Extract frames from the uploaded video.
        """

        logger.info("Frame extraction started.")

        frames = self.frame_extractor.extract(video_path)

        logger.info("Frame extraction completed.")

        logger.info(
            "Total Frames Extracted : %d",
            len(frames),
        )

        return frames

    # ==========================================================
    # OCR
    # ==========================================================

    def extract_ocr(
        self,
        frames: list[Path],
    ) -> list[dict]:
        """
        Run OCR on all extracted frames.
        """

        logger.info("OCR processing started.")

        results = []

        for frame in frames:

            result = self.ocr_processor.extract_text(frame)

            results.append(
                {
                    "frame": frame,
                    "text": result["text"],
                    "confidence": result["confidence"],
                }
            )

        logger.info("OCR processing completed.")

        logger.info(
            "OCR completed for %d frames.",
            len(results),
        )

        return results

    # ==========================================================
    # BLIP Caption Generation
    # ==========================================================

    def generate_captions(
        self,
        frames: list[Path],
    ) -> list[dict]:
        """
        Generate captions for all extracted frames.
        """

        logger.info("BLIP caption generation started.")

        captions = []

        for frame in frames:

            caption = self.caption_generator.generate_caption(frame)

            captions.append(
                {
                    "frame": frame,
                    "caption": caption,
                }
            )

        logger.info("BLIP caption generation completed.")

        logger.info(
            "Generated captions for %d frames.",
            len(captions),
        )

        return captions