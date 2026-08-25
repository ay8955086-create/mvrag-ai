import apiClient from './api';
import { VideoResponse, ExtendedVideoDetails } from '../types';

type BackendVideoDetails = VideoResponse & {
  transcripts?: ExtendedVideoDetails['transcripts'];
  ocr_results?: ExtendedVideoDetails['ocr_results'];
  captions?: ExtendedVideoDetails['captions'];
  chunks?: ExtendedVideoDetails['chunks'];
  processing_stats?: ExtendedVideoDetails['processing_stats'];
};

export const videoService = {
  async uploadVideo(
    file: File,
    title: string,
    description?: string,
    onUploadProgress?: (progressEvent: any) => void,
  ): Promise<VideoResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);

    if (description) {
      formData.append('description', description);
    }

    const response = await apiClient.post<VideoResponse>(
      '/videos/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
      },
    );

    return response.data;
  },

  async getVideos(): Promise<VideoResponse[]> {
    const response = await apiClient.get<VideoResponse[]>('/videos');
    return response.data;
  },

  async getVideoById(videoId: number): Promise<VideoResponse> {
    const response = await apiClient.get<VideoResponse>(`/videos/${videoId}`);
    return response.data;
  },

  async deleteVideo(videoId: number): Promise<{ message: string }> {
    const response = await apiClient.delete<{ message: string }>(
      `/videos/${videoId}`,
    );
    return response.data;
  },

  /**
   * Normalize details returned by the backend.
   *
   * Important: this function no longer fabricates transcript/OCR/BLIP/chunk
   * content. Missing backend data remains empty so the UI never presents
   * synthetic information as if it came from the video.
   */
  getExtendedDetails(video: VideoResponse): ExtendedVideoDetails {
    const backendVideo = video as BackendVideoDetails;

    return {
      ...video,
      transcripts: backendVideo.transcripts ?? [],
      ocr_results: backendVideo.ocr_results ?? [],
      captions: backendVideo.captions ?? [],
      chunks: backendVideo.chunks ?? [],
      processing_stats: backendVideo.processing_stats,
    };
  },
};
