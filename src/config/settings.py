"""
Application configuration management for MVRAG AI.

This module centralizes all application settings loaded from the
environment and provides validated, strongly typed configuration
throughout the project.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# -----------------------------------------------------------------------------
# Project Root
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------

    APP_NAME: str = Field(...)
    APP_VERSION: str = Field(...)
    APP_ENV: str = Field(...)
    DEBUG: bool = Field(default=False)

    # -------------------------------------------------------------------------
    # Directories
    # -------------------------------------------------------------------------

    DATA_DIR: str
    LOG_DIR: str
    VECTOR_DB_DIR: str

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    LOG_LEVEL: str
    LOG_FILE: str

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    DATABASE_URL: str

    # -------------------------------------------------------------------------
    # Vector Database
    # -------------------------------------------------------------------------

    VECTOR_DB_NAME: str

    # -------------------------------------------------------------------------
    # Embedding Models
    # -------------------------------------------------------------------------

    EMBEDDING_MODEL: str
    RERANKER_MODEL: str

    # -------------------------------------------------------------------------
    # AI Models
    # -------------------------------------------------------------------------

    WHISPER_MODEL: str
    OCR_LANGUAGE: str
    IMAGE_CAPTION_MODEL: str
    FRAME_INTERVAL_SECONDS: int = 10

    # -------------------------------------------------------------------------
    # LLM
    # -------------------------------------------------------------------------

    LLM_PROVIDER: str

    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    LLM_MODEL: str
    OLLAMA_BASE_URL: str = ""

    # -------------------------------------------------------------------------
    # Retrieval
    # -------------------------------------------------------------------------

    TOP_K_RESULTS: int
    SIMILARITY_THRESHOLD: float

    # -------------------------------------------------------------------------
    # Path Helpers
    # -------------------------------------------------------------------------

    @property
    def root_dir(self) -> Path:
        return PROJECT_ROOT

    @property
    def data_dir(self) -> Path:
        return self.root_dir / self.DATA_DIR

    @property
    def logs_dir(self) -> Path:
        return self.root_dir / self.LOG_DIR

    @property
    def vector_db_dir(self) -> Path:
        return self.root_dir / self.VECTOR_DB_DIR

    @property
    def raw_video_dir(self) -> Path:
        return self.data_dir / "raw_videos"

    @property
    def audio_dir(self) -> Path:
        return self.data_dir / "audio"

    @property
    def frames_dir(self) -> Path:
        return self.data_dir / "frames"

    @property
    def keyframes_dir(self) -> Path:
        return self.data_dir / "keyframes"

    @property
    def transcripts_dir(self) -> Path:
        return self.data_dir / "transcripts"

    @property
    def captions_dir(self) -> Path:
        return self.data_dir / "captions"

    @property
    def ocr_dir(self) -> Path:
        return self.data_dir / "ocr"

    @property
    def thumbnails_dir(self) -> Path:
        return self.data_dir / "thumbnails"

    @property
    def processed_chunks_dir(self) -> Path:
        return self.data_dir / "processed_chunks"

    @property
    def exports_dir(self) -> Path:
        return self.data_dir / "exports"

    # -------------------------------------------------------------------------
    # Directory Creation
    # -------------------------------------------------------------------------

    def create_directories(self) -> None:
        """
        Create every directory required by the application.
        Safe to call multiple times.
        """

        directories = [
            self.data_dir,
            self.logs_dir,
            self.vector_db_dir,
            self.raw_video_dir,
            self.audio_dir,
            self.frames_dir,
            self.keyframes_dir,
            self.transcripts_dir,
            self.captions_dir,
            self.ocr_dir,
            self.thumbnails_dir,
            self.processed_chunks_dir,
            self.exports_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Cached Settings Instance
# -----------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    settings = Settings()
    settings.create_directories()
    return settings


settings = get_settings()