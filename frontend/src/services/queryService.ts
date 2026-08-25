import apiClient from './api';
import { APIResponse, QueryResponseData } from '../types';

export const queryService = {
  /**
   * Ask a question over the indexed video repository.
   *
   * videoId is optional. When supplied, the backend should restrict
   * retrieval to that video.
   */
  async askQuestion(
    question: string,
    videoId?: number | null,
  ): Promise<QueryResponseData> {
    const payload: {
      question: string;
      video_id?: number;
    } = {
      question,
    };

    if (videoId !== undefined && videoId !== null && !Number.isNaN(videoId)) {
      payload.video_id = videoId;
    }

    const response = await apiClient.post<APIResponse<QueryResponseData>>(
      '/query',
      payload,
    );

    return response.data.data;
  },
};
