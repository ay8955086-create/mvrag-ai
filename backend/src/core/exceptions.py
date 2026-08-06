"""
Custom exception hierarchy for MVRAG AI.

Every custom exception in the project should inherit from
MVRAGException to provide consistent error handling.
"""

from __future__ import annotations

from typing import Any


class MVRAGException(Exception):
    """
    Base exception for all custom exceptions in MVRAG AI.
    """

    def __init__(
        self,
        message: str,
        *,
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.details = details
        super().__init__(message)

    def __str__(self) -> str:
        if self.details is None:
            return self.message
        return f"{self.message} | Details: {self.details}"


# =============================================================================
# Configuration
# =============================================================================


class ConfigurationError(MVRAGException):
    """
    Raised when application configuration is invalid.
    """


# =============================================================================
# File System
# =============================================================================


class FileOperationError(MVRAGException):
    """
    Raised when a file operation fails.
    """


class InvalidFileError(MVRAGException):
    """
    Raised when an uploaded file is invalid.
    """


class UnsupportedFileTypeError(MVRAGException):
    """
    Raised when the uploaded file format is not supported.
    """


class FileTooLargeError(MVRAGException):
    """
    Raised when the uploaded file exceeds the allowed size.
    """


# =============================================================================
# Video Processing
# =============================================================================


class VideoProcessingError(MVRAGException):
    """
    Raised when video processing fails.
    """


class AudioExtractionError(VideoProcessingError):
    """
    Raised when audio extraction fails.
    """


class FrameExtractionError(VideoProcessingError):
    """
    Raised when frame extraction fails.
    """


class ThumbnailGenerationError(VideoProcessingError):
    """
    Raised when thumbnail generation fails.
    """


# =============================================================================
# AI Processing
# =============================================================================


class SpeechRecognitionError(MVRAGException):
    """
    Raised when Whisper transcription fails.
    """


class OCRError(MVRAGException):
    """
    Raised when OCR processing fails.
    """


class ImageCaptionError(MVRAGException):
    """
    Raised when image caption generation fails.
    """


# =============================================================================
# Embeddings
# =============================================================================


class EmbeddingError(MVRAGException):
    """
    Raised when embedding generation fails.
    """


class VectorDatabaseError(MVRAGException):
    """
    Raised when vector database operations fail.
    """


# =============================================================================
# Retrieval
# =============================================================================


class RetrievalError(MVRAGException):
    """
    Raised when retrieval fails.
    """


class RerankingError(MVRAGException):
    """
    Raised when reranking fails.
    """


# =============================================================================
# LLM
# =============================================================================


class LLMError(MVRAGException):
    """
    Raised when an LLM request fails.
    """


class PromptGenerationError(MVRAGException):
    """
    Raised when prompt generation fails.
    """


class ResponseGenerationError(MVRAGException):
    """
    Raised when answer generation fails.
    """


# =============================================================================
# Database
# =============================================================================


class DatabaseError(MVRAGException):
    """
    Raised when a database operation fails.
    """


class RecordNotFoundError(DatabaseError):
    """
    Raised when a requested record does not exist.
    """


# =============================================================================
# API
# =============================================================================


class APIError(MVRAGException):
    """
    Raised for API-related failures.
    """


class AuthenticationError(APIError):
    """
    Raised when authentication fails.
    """


class AuthorizationError(APIError):
    """
    Raised when authorization fails.
    """


class ValidationError(APIError):
    """
    Raised when request validation fails.
    """


# =============================================================================
# Pipeline
# =============================================================================


class PipelineError(MVRAGException):
    """
    Raised when the processing pipeline fails.
    """


class ServiceError(MVRAGException):
    """
    Raised when a service layer operation fails.
    """


class ModelLoadError(MVRAGException):
    """
    Raised when an AI model cannot be loaded.
    """


class DependencyError(MVRAGException):
    """
    Raised when a required external dependency is unavailable.
    """