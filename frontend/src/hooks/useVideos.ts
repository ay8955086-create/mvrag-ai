import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { videoService } from '../services/videoService';
import { VideoResponse } from '../types';
import { toast } from 'sonner';

export const QUERY_KEYS = {
  videos: ['videos'] as const,
  video: (id: number) => ['video', id] as const,
};

export const useVideos = () => {
  return useQuery<VideoResponse[], Error>({
    queryKey: QUERY_KEYS.videos,
    queryFn: videoService.getVideos,
    refetchInterval: 5000, // Poll every 5 seconds to track background video processing status
  });
};

export const useVideo = (videoId: number) => {
  return useQuery<VideoResponse, Error>({
    queryKey: QUERY_KEYS.video(videoId),
    queryFn: () => videoService.getVideoById(videoId),
    enabled: !!videoId && !isNaN(videoId),
    refetchInterval: (query) => {
      // Poll faster if status is Processing or Pending
      const data = query.state.data;
      if (data && (data.status === 'Processing' || data.status === 'Pending')) {
        return 2000;
      }
      return false;
    },
  });
};

export const useUploadVideo = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      file,
      title,
      description,
      onProgress,
    }: {
      file: File;
      title: string;
      description?: string;
      onProgress?: (progress: number) => void;
    }) => {
      return videoService.uploadVideo(file, title, description, (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      });
    },
    onSuccess: (data) => {
      toast.success(`Video "${data.title}" uploaded successfully!`);
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.videos });
    },
    onError: (error: Error) => {
      toast.error(`Upload failed: ${error.message}`);
    },
  });
};

export const useDeleteVideo = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (videoId: number) => videoService.deleteVideo(videoId),
    onSuccess: () => {
      toast.success('Video deleted successfully.');
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.videos });
    },
    onError: (error: Error) => {
      toast.error(`Failed to delete video: ${error.message}`);
    },
  });
};
