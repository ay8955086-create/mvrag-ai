"""
Main processing pipeline for MVRAG AI.

This module orchestrates the complete video processing workflow.
"""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from src.models.analytics import Analytics
from src.models.caption import Caption
from src.models.chunk import Chunk
from src.models.ocr import OCRResult
from src.models.transcript import Transcript

from src.core.logger import get_logger
from src.embeddings.chroma_store import ChromaStore
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.models.frame_info import FrameInfo
from src.processors.audio.audio_extractor import AudioExtractor
from src.processors.caption.caption_generator import CaptionGenerator
from src.processors.chunking.chunk_generator import ChunkGenerator
from src.processors.frames.frame_extractor import FrameExtractor
from src.processors.ocr.ocr_processor import OCRProcessor
from src.processors.whisper.transcriber import WhisperTranscriber
from src.utils.video_metadata import extract_video_metadata

logger = get_logger(__name__)


class VideoPipeline:
    """
    Executes the complete AI pipeline for one uploaded video.
    """

    def __init__(
        self,
        db: Session | None = None,
        video_id: int | None = None,
    ):
        """
        Initialize all pipeline components.

        db and video_id are optional so the pipeline remains reusable
        outside the background API workflow.
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

        logger.info(
            "VideoPipeline initialized."
        )

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

        started_at = perf_counter()

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(
                video_path
            )

        logger.info("=" * 60)

        logger.info(
            "Processing video: %s",
            video_path.name,
        )

        # ------------------------------------------------------
        # Step 1: Metadata
        # ------------------------------------------------------

        metadata = self.extract_metadata(
            video_path
        )

        # ------------------------------------------------------
        # Step 2: Audio
        # ------------------------------------------------------

        audio_path = self.extract_audio(
            video_path
        )

        # ------------------------------------------------------
        # Step 3: Whisper
        # ------------------------------------------------------

        transcript = self.transcribe(
            audio_path
        )

        # ------------------------------------------------------
        # Step 4: Frames
        # ------------------------------------------------------

        frames = self.extract_frames(
            video_path
        )

        # ------------------------------------------------------
        # Step 5: OCR
        # ------------------------------------------------------

        ocr_results = self.extract_ocr(
            frames
        )

        # ------------------------------------------------------
        # Step 6: BLIP
        # ------------------------------------------------------

        captions = self.generate_captions(
            frames
        )

        # ------------------------------------------------------
        # Step 7: Semantic Chunks
        # ------------------------------------------------------

        chunks = self.generate_chunks(
            transcript,
            ocr_results,
            captions,
        )

        # ------------------------------------------------------
        # Step 8: Embeddings + ChromaDB
        # ------------------------------------------------------

        stored_chunks = self.store_embeddings(
            chunks
        )

        if self.db is not None and self.video_id is not None:
            self.persist_results(
                transcript=transcript,
                ocr_results=ocr_results,
                captions=captions,
                chunks=stored_chunks,
                processing_time=perf_counter() - started_at,
            )

        logger.info("=" * 60)

        logger.info(
            "Video processing completed successfully."
        )

        return {
            "metadata": metadata,
            "audio_path": audio_path,
            "transcript": transcript,
            "frames": frames,
            "ocr": ocr_results,
            "captions": captions,
            "chunks": stored_chunks,
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

        logger.info(
            "Metadata extraction started."
        )

        metadata = extract_video_metadata(
            str(video_path)
        )

        logger.info(
            "Metadata extracted successfully."
        )

        logger.info(
            "Duration : %.2f sec | FPS : %.2f | "
            "Resolution : %dx%d | Size : %.2f MB",
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

        logger.info(
            "Audio extraction started."
        )

        audio_path = (
            self.audio_extractor.extract(
                video_path
            )
        )

        logger.info(
            "Audio extraction completed."
        )

        logger.info(
            "Audio saved at: %s",
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

        logger.info(
            "Whisper transcription started."
        )

        result = self.whisper.transcribe(
            audio_path
        )

        logger.info(
            "Whisper transcription completed."
        )

        logger.info(
            "Detected Language: %s",
            result.get(
                "language",
                "unknown",
            ),
        )

        logger.info(
            "Transcript Segments: %d",
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

        logger.info(
            "Frame extraction started."
        )

        frames = self.frame_extractor.extract(
            video_path
        )

        logger.info(
            "Frame extraction completed."
        )

        logger.info(
            "Total Frames Extracted: %d",
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

        logger.info(
            "OCR processing started."
        )

        results: list[dict] = []

        for frame_info in frames:

            result = (
                self.ocr_processor.extract_text(
                    frame_info.frame
                )
            )

            results.append(
                {
                    "frame": frame_info.frame,
                    "timestamp": frame_info.timestamp,
                    "text": result["text"],
                    "confidence": result["confidence"],
                }
            )

        logger.info(
            "OCR processing completed."
        )

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

        logger.info(
            "BLIP caption generation started."
        )

        captions: list[dict] = []

        for frame_info in frames:

            caption = (
                self.caption_generator.generate_caption(
                    frame_info.frame
                )
            )

            captions.append(
                {
                    "frame": frame_info.frame,
                    "timestamp": frame_info.timestamp,
                    "caption": caption,
                }
            )

        logger.info(
            "BLIP caption generation completed."
        )

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

        logger.info(
            "Semantic chunk generation started."
        )

        chunks = (
            self.chunk_generator.generate_chunks(
                transcript_segments=transcript[
                    "segments"
                ],
                ocr_results=ocr_results,
                captions=captions,
            )
        )

        logger.info(
            "Semantic chunk generation completed."
        )

        logger.info(
            "Generated %d semantic chunks.",
            len(chunks),
        )

        return chunks



        # ==========================================================
    # Embedding Generation + ChromaDB
    # ==========================================================

    def store_embeddings(
        self,
        chunks,
    ):
        """
        Generate embeddings in batches and store
        them in ChromaDB.
        """

        logger.info("Embedding generation started.")

        if not chunks:
            logger.warning(
                "No chunks available for embedding."
            )
            return chunks

        # ------------------------------------------------------
        # Prepare texts
        # ------------------------------------------------------

        texts = [
            chunk.combined_text
            for chunk in chunks
        ]

        logger.info(
            "Preparing %d chunks for batch embedding.",
            len(texts),
        )

        # ------------------------------------------------------
        # Generate batch embeddings
        # ------------------------------------------------------

        embeddings = (
            self.embedding_generator.generate_embeddings(
                texts,
                batch_size=16,
            )
        )

        if len(embeddings) != len(chunks):
            raise RuntimeError(
                "Number of generated embeddings does not "
                "match number of chunks."
            )

        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )

        # ------------------------------------------------------
        # Generate deterministic IDs
        # ------------------------------------------------------

        embedding_ids = [
            f"video_{self.video_id}_chunk_{chunk.chunk_index}"
            for chunk in chunks
        ]

        # ------------------------------------------------------
        # Store ID on EVERY chunk
        # ------------------------------------------------------

        for chunk, embedding_id in zip(
            chunks,
            embedding_ids,
        ):
            chunk.embedding_id = embedding_id

        # ------------------------------------------------------
        # Prepare documents
        # ------------------------------------------------------

        documents = [
            chunk.combined_text
            for chunk in chunks
        ]

        # ------------------------------------------------------
        # Prepare metadata
        # ------------------------------------------------------

        metadatas = [
            {
                "video_id": int(self.video_id),
                "chunk_index": chunk.chunk_index,
                "start_time": float(chunk.start_time),
                "end_time": float(chunk.end_time),
            }
            for chunk in chunks
        ]

        # ------------------------------------------------------
        # Store embeddings in ChromaDB
        # ------------------------------------------------------

        logger.info(
            "Starting ChromaDB indexing."
        )

        self.chroma_store.add_embeddings(
            ids=embedding_ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info(
            "Stored %d embeddings in ChromaDB.",
            len(chunks),
        )

        logger.info(
            "ChromaDB indexing completed successfully."
        )

        return chunks
    # ==========================================================
    # Database Persistence
    # ==========================================================

    def persist_results(
        self,
        transcript: dict,
        ocr_results: list[dict],
        captions: list[dict],
        chunks,
        processing_time: float,
    ) -> None:
        """Persist all extracted multimodal results for the video."""

        if self.db is None or self.video_id is None:
            return

        video_id = int(self.video_id)

        logger.info(
            "Persisting processing results for video %d.",
            video_id,
        )

        self.db.query(Transcript).filter(
            Transcript.video_id == video_id
        ).delete(synchronize_session=False)

        self.db.query(OCRResult).filter(
            OCRResult.video_id == video_id
        ).delete(synchronize_session=False)

        self.db.query(Caption).filter(
            Caption.video_id == video_id
        ).delete(synchronize_session=False)

        self.db.query(Chunk).filter(
            Chunk.video_id == video_id
        ).delete(synchronize_session=False)

        self.db.query(Analytics).filter(
            Analytics.video_id == video_id
        ).delete(synchronize_session=False)

        transcript_rows = [
            Transcript(
                video_id=video_id,
                start_time=float(segment["start"]),
                end_time=float(segment["end"]),
                text=str(segment.get("text", "")).strip(),
                language=str(transcript.get("language", "en")),
                confidence=1.0,
            )
            for segment in transcript.get("segments", [])
        ]
        self.db.add_all(transcript_rows)

        ocr_rows = [
            OCRResult(
                video_id=video_id,
                frame_number=index,
                timestamp=float(item["timestamp"]),
                text=str(item.get("text", "")),
                confidence=float(item.get("confidence", 0.0)),
            )
            for index, item in enumerate(ocr_results)
        ]
        self.db.add_all(ocr_rows)

        caption_rows = [
            Caption(
                video_id=video_id,
                frame_number=index,
                timestamp=float(item["timestamp"]),
                caption=str(item.get("caption", "")),
            )
            for index, item in enumerate(captions)
        ]
        self.db.add_all(caption_rows)

        chunk_rows = [
            Chunk(
                video_id=video_id,
                chunk_index=int(chunk.chunk_index),
                start_time=float(chunk.start_time),
                end_time=float(chunk.end_time),
                transcript=str(chunk.transcript),
                ocr_text=str(chunk.ocr_text),
                caption=str(chunk.caption),
                combined_text=str(chunk.combined_text),
                embedding_id=getattr(chunk, "embedding_id", None),
            )
            for chunk in chunks
        ]
        self.db.add_all(chunk_rows)

        self.db.add(
            Analytics(
                video_id=video_id,
                processing_time=float(processing_time),
                transcript_segments=len(transcript_rows),
                ocr_detections=len(ocr_rows),
                caption_count=len(caption_rows),
                chunk_count=len(chunk_rows),
                total_queries=0,
                average_response_time=0.0,
            )
        )

        self.db.commit()

        logger.info(
            "Persisted %d transcripts, %d OCR results, %d captions "
            "and %d chunks for video %d.",
            len(transcript_rows),
            len(ocr_rows),
            len(caption_rows),
            len(chunk_rows),
            video_id,
        )
