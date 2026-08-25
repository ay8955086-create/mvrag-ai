from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TranscriptResponse(BaseModel):
    id: int
    start_time: float
    end_time: float
    text: str
    language: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)


class OCRResponse(BaseModel):
    id: int
    frame_number: int
    timestamp: float
    text: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)


class CaptionResponse(BaseModel):
    id: int
    frame_number: int
    timestamp: float
    caption: str

    model_config = ConfigDict(from_attributes=True)


class ChunkResponse(BaseModel):
    id: int
    chunk_index: int
    start_time: float
    end_time: float
    transcript: str
    ocr_text: str
    caption: str
    combined_text: str
    embedding_id: str | None

    model_config = ConfigDict(from_attributes=True)


class ProcessingStatsResponse(BaseModel):
    processing_time: float
    transcript_segments: int
    ocr_detections: int
    caption_count: int
    chunk_count: int
    total_queries: int
    average_response_time: float

    model_config = ConfigDict(from_attributes=True)


class VideoResponse(BaseModel):
    id: int
    filename: str
    title: str
    description: str | None

    duration: float
    fps: float
    width: int
    height: int
    size_mb: float

    status: str
    upload_time: datetime
    processed_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ExtendedVideoResponse(VideoResponse):
    transcripts: list[TranscriptResponse] = []
    ocr_results: list[OCRResponse] = []
    captions: list[CaptionResponse] = []
    chunks: list[ChunkResponse] = []
    processing_stats: ProcessingStatsResponse | None = None
