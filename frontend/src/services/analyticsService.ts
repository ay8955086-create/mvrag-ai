import apiClient from './api';
import { AnalyticsResponse } from '../types';

export const analyticsService = {
  /**
   * Get application analytics & dashboard statistics
   */
  async getDashboardAnalytics(): Promise<AnalyticsResponse> {
    const response = await apiClient.get<AnalyticsResponse>('/analytics');
    return response.data;
  },
};
