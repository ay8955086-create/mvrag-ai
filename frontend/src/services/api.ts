import axios from 'axios';

export const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const MEDIA_BASE_URL =
  import.meta.env.VITE_MEDIA_BASE_URL || `${BASE_URL}/media`;

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000,
});

export const getVideoMediaUrl = (filename: string): string => {
  const safeFilename = encodeURIComponent(filename);
  return `${MEDIA_BASE_URL.replace(/\/$/, '')}/videos/${safeFilename}`;
};

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred';

    return Promise.reject(new Error(message));
  },
);

export default apiClient;
