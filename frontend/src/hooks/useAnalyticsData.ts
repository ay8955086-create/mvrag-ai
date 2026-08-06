import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '../services/analyticsService';
import { AnalyticsResponse } from '../types';

export const useAnalyticsData = () => {
  return useQuery<AnalyticsResponse, Error>({
    queryKey: ['analytics'],
    queryFn: analyticsService.getDashboardAnalytics,
    refetchInterval: 10000,
  });
};
