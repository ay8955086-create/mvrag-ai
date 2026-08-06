import apiClient from './api';
import { APIResponse, QueryResponseData } from '../types';

export const queryService = {
  /**
   * Ask a question over the indexed video repository (RAG pipeline)
   */
  async askQuestion(question: string): Promise<QueryResponseData> {
    const response = await apiClient.post<APIResponse<QueryResponseData>>('/query', {
      question,
    });
    return response.data.data;
  },
};
