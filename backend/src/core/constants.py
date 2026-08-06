"""
Global constants used throughout MVRAG AI.

This module centralizes application-wide constants to avoid hard-coded
values and improve maintainability.
"""

from pathlib import Path

# =============================================================================
# Application Information
# =============================================================================

APP_DISPLAY_NAME = "MVRAG AI"
APP_SHORT_NAME = "MVRAG"
APP_DESCRIPTION = "Multimodal Video Retrieval-Augmented Generation"

# =============================================================================
# Version Information
# =============================================================================

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# =============================================================================
# File Extensions
# =============================================================================

VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".wmv",
    ".flv",
    ".webm",
    ".mpeg",
    ".mpg",
    ".m4v",
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".m4a",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".webp",
}

# =============================================================================
# MIME Types
# =============================================================================

VIDEO_MIME_TYPES = {
    "video/mp4",
    "video/x-msvideo",
    "video/x-matroska",
    "video/quicktime",
    "video/webm",
}

# =============================================================================
# Processing
# =============================================================================

FRAME_EXTRACTION_INTERVAL = 2          # seconds
DEFAULT_CHUNK_DURATION = 30            # seconds
MIN_CHUNK_DURATION = 10                # seconds
MAX_CHUNK_DURATION = 60                # seconds

DEFAULT_BATCH_SIZE = 16

# =============================================================================
# Embeddings
# =============================================================================

EMBEDDING_DIMENSION = 1024

DEFAULT_TOP_K = 5
MAX_TOP_K = 20

# =============================================================================
# Similarity
# =============================================================================

DEFAULT_SIMILARITY_THRESHOLD = 0.70

# =============================================================================
# Timestamp Format
# =============================================================================

TIMESTAMP_FORMAT = "%H:%M:%S"

# =============================================================================
# Database
# =============================================================================

SQLITE_DATABASE_NAME = "mvrag.db"

CHROMA_COLLECTION_NAME = "video_embeddings"

# =============================================================================
# Logging
# =============================================================================

LOGGER_NAME = "MVRAG"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_LOG_FILE_SIZE = 10 * 1024 * 1024      # 10 MB

LOG_BACKUP_COUNT = 5

# =============================================================================
# Upload Limits
# =============================================================================

MAX_VIDEO_SIZE_MB = 2048

MAX_FILENAME_LENGTH = 255

# =============================================================================
# UI
# =============================================================================

SUPPORTED_THEME = {
    "light",
    "dark",
}

DEFAULT_PAGE_SIZE = 10

# =============================================================================
# Health Check
# =============================================================================

HEALTH_STATUS_OK = "OK"

HEALTH_STATUS_ERROR = "ERROR"

# =============================================================================
# Processing Status
# =============================================================================

STATUS_PENDING = "Pending"

STATUS_PROCESSING = "Processing"

STATUS_COMPLETED = "Completed"

STATUS_FAILED = "Failed"

# =============================================================================
# AI Providers
# =============================================================================

LLM_OPENAI = "openai"

LLM_GEMINI = "gemini"

LLM_OLLAMA = "ollama"

SUPPORTED_LLM_PROVIDERS = {
    LLM_OPENAI,
    LLM_GEMINI,
    LLM_OLLAMA,
}

# =============================================================================
# Cache
# =============================================================================

CACHE_DIRECTORY = Path(".cache")

MODEL_CACHE_DIRECTORY = CACHE_DIRECTORY / "models"

EMBEDDING_CACHE_DIRECTORY = CACHE_DIRECTORY / "embeddings"