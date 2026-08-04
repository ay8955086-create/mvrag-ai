"""
Main processing pipeline...
"""

from __future__ import annotations

from uuid import uuid4
from pathlib import Path

from src.embeddings.embedding_generator import EmbeddingGenerator
from src.embeddings.chroma_store import ChromaStore

from src.core.logger import get_logger
from src.utils.video_metadata import extract_video_metadata

from src.models.frame_info import FrameInfo

from src.processors.audio.audio_extractor import AudioExtractor
from src.processors.whisper.transcriber import WhisperTranscriber
from src.processors.frames.frame_extractor import FrameExtractor
from src.processors.ocr.ocr_processor import OCRProcessor
from src.processors.caption.caption_generator import CaptionGenerator
from src.processors.chunking.chunk_generator import ChunkGenerator
from sqlalchemy.orm import Session

from src.models.processing_status import ProcessingStatus

logger = get_logger(__name__)


class VideoPipeline:
    """
    Executes the complete AI pipeline for one uploaded video.
    """

    def __init__(
    self,
    db: Session,
    video_id: int,
):
        """
        Initialize all pipeline components.
        """
        self.db = db

        self.video_id = video_id

        self.audio_extractor = AudioExtractor()

        self.whisper = WhisperTranscriber()

        self.frame_extractor = FrameExtractor()

        self.ocr_processor = OCRProcessor()

        self.caption_generator = CaptionGenerator()

        self.chunk_generator = ChunkGenerator()

        self.embedding_generator = EmbeddingGenerator()

        self.chroma_store = ChromaStore()

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

    try:

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(video_path)

        logger.info("=" * 60)
        logger.info("Processing video: %s", video_path.name)

        # ------------------------------------------------------
        # Step 1 : Metadata
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Extracting Metadata",
            10,
        )

        metadata = self.extract_metadata(video_path)

        # ------------------------------------------------------
        # Step 2 : Audio
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Extracting Audio",
            20,
        )

        audio_path = self.extract_audio(video_path)

        # ------------------------------------------------------
        # Step 3 : Whisper
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Running Whisper",
            35,
        )

        transcript = self.transcribe(audio_path)

        # ------------------------------------------------------
        # Step 4 : Frames
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Extracting Frames",
            50,
        )

        frames = self.extract_frames(video_path)

        # ------------------------------------------------------
        # Step 5 : OCR
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Running OCR",
            65,
        )

        ocr_results = self.extract_ocr(frames)

        # ------------------------------------------------------
        # Step 6 : BLIP
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Generating Captions",
            75,
        )

        captions = self.generate_captions(frames)

        # ------------------------------------------------------
        # Step 7 : Chunking
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Generating Chunks",
            85,
        )

        chunks = self.generate_chunks(
            transcript,
            ocr_results,
            captions,
        )

        # ------------------------------------------------------
        # Step 8 : Embeddings
        # ------------------------------------------------------

        self._update_progress(
            "Processing",
            "Generating Embeddings",
            95,
        )

        stored_chunks = self.store_embeddings(chunks)

        # ------------------------------------------------------
        # Completed
        # ------------------------------------------------------

        self._set_completed()

        logger.info("=" * 60)
        logger.info("Video processing completed successfully.")

        return {
            "metadata": metadata,
            "audio_path": audio_path,
            "transcript": transcript,
            "frames": frames,
            "ocr": ocr_results,
            "captions": captions,
            "chunks": stored_chunks,
        }

    except Exception as error:

        self._set_failed(error)

        raise

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

        logger.info(
            "Audio saved at : %s",
            audio_path,
        )

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
            result.get(
                "language",
                "unknown",
            ),
        )

        logger.info(
            "Transcript Segments : %d",
            len(
                result.get(
                    "segments",
                    [],
                )
            ),
        )

        return result

    # ==========================================================
    # Frame Extraction
    # ==========================================================

    def extract_frames(
        self,
        video_path: Path,
    ) -> list[FrameInfo]:
        """
        Extract frames from the uploaded video.
        """

        logger.info("Frame extraction started.")

        frames = self.frame_extractor.extract(
            video_path,
        )

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
        frames: list[FrameInfo],
    ) -> list[dict]:
        """
        Run OCR on all extracted frames.
        """

        logger.info("OCR processing started.")

        results = []

        for frame_info in frames:

            result = self.ocr_processor.extract_text(
                frame_info.frame,
            )

            results.append(
                {
                    "frame": frame_info.frame,
                    "timestamp": frame_info.timestamp,
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
        frames: list[FrameInfo],
    ) -> list[dict]:
        """
        Generate captions for all extracted frames.
        """

        logger.info("BLIP caption generation started.")

        captions = []

        for frame_info in frames:

            caption = self.caption_generator.generate_caption(
                frame_info.frame,
            )

            captions.append(
                {
                    "frame": frame_info.frame,
                    "timestamp": frame_info.timestamp,
                    "caption": caption,
                }
            )

        logger.info("BLIP caption generation completed.")

        logger.info(
            "Generated captions for %d frames.",
            len(captions),
        )

        return captions

    # ==========================================================
    # Semantic Chunk Generation
    # ==========================================================

    def generate_chunks(
        self,
        transcript: dict,
        ocr_results: list[dict],
        captions: list[dict],
    ):
        """
        Generate semantic chunks.
        """

        logger.info("Semantic chunk generation started.")

        chunks = self.chunk_generator.generate_chunks(
            transcript_segments=transcript["segments"],
            ocr_results=ocr_results,
            captions=captions,
        )

        logger.info("Semantic chunk generation completed.")

        logger.info(
            "Generated %d semantic chunks.",
            len(chunks),
        )

        return chunks

def store_embeddings(
    self,
    chunks,
):
    """
    Generate embeddings and store them in ChromaDB.
    """

    logger.info("Embedding generation started.")

    for chunk in chunks:

        embedding = self.embedding_generator.generate_embedding(
            chunk.combined_text,
        )

        embedding_id = str(uuid4())

        self.chroma_store.add_embedding(
            embedding_id=embedding_id,
            embedding=embedding,
            document=chunk.combined_text,
            metadata={
                "chunk_index": chunk.chunk_index,
                "start_time": chunk.start_time,
                "end_time": chunk.end_time,
            },
        )

        if hasattr(chunk, "embedding_id"):
            chunk.embedding_id = embedding_id

    logger.info(
        "Stored %d embeddings in ChromaDB.",
        len(chunks),
    )

    return chunks