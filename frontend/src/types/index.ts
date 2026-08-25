// Video status types matching FastAPI Video models
export type VideoStatus = 'Pending' | 'Processing' | 'Completed' | 'Failed';

export interface VideoResponse {
  id: number;
  filename: string;
  title: string;
  description: string | null;
  duration: number;
  fps: number;
  width: number;
  height: number;
  size_mb: number;
  status: VideoStatus;
  upload_time: string;
  processed_time?: string | null;
}

export interface VideoCreateRequest {
  title: string;
  description?: string;
  file: File;
}

export interface QueryRequest {
  question: string;
  video_id?: number | null;
}

export interface ContextChunk {
  document: string;
  score?: number;
  distance?: number;
  start_time?: number;
  end_time?: number;
  chunk_index?: number;
  video_id?: number;
  transcript?: string;
  ocr_text?: string;
  caption?: string;
  metadata?: Record<string, unknown>;
}

export interface QueryResponseData {
  question: string;
  context: ContextChunk[];
  answer: string;
}

export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
}

export interface AnalyticsResponse {
  total_videos: number;
  total_chunks: number;
  completed: number;
  processing: number;
  failed: number;
}

export interface ExtendedVideoDetails extends VideoResponse {
  transcripts?: Array<{
    id: number;
    start_time: number;
    end_time: number;
    text: string;
    language: string;
    confidence: number;
  }>;
  ocr_results?: Array<{
    id: number;
    frame_number: number;
    timestamp: number;
    text: string;
    confidence: number;
  }>;
  captions?: Array<{
    id: number;
    frame_number: number;
    timestamp: number;
    caption: string;
  }>;
  chunks?: Array<{
    id: number;
    chunk_index: number;
    start_time: number;
    end_time: number;
    transcript: string;
    ocr_text: string;
    caption: string;
    combined_text: string;
    embedding_id?: string;
  }>;
  processing_stats?: {
    processing_time: number;
    transcript_segments: number;
    ocr_detections: number;
    caption_count: number;
    chunk_count: number;
    total_queries: number;
    average_response_time: number;
  };
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
  sources?: ContextChunk[];
}

export interface PipelineStep {
  id: string;
  label: string;
  description: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  icon: string;
}
