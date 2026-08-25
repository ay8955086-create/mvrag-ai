# MVRAG Frontend - Module 1 Integration Fix

This module fixes the frontend-side integration problems without changing the video-processing pipeline.

Changes:
1. VideoPlayer now builds a browser media URL instead of using a filesystem-style `/api/data/raw_videos/...` URL.
2. AI Chat sends `video_id` when a specific video is selected.
3. Removed fabricated transcript/OCR/BLIP/chunk data from `videoService.getExtendedDetails()`.
4. Citation cards no longer fake 85% scores or 00:00 timestamps.
5. Search no longer assumes the first video is the source of every result.
6. Query types now support video-scoped retrieval and multimodal source fields.

IMPORTANT:
The frontend now expects the backend to expose:
    GET /media/videos/{filename}

With the default frontend API URL, a video is expected at:
    http://localhost:8000/media/videos/<filename>

If your backend does not yet expose this route, the video player will still show an error until that backend endpoint is added.

After extracting these files into D:\MVRAG\frontend, run:
    npm install
    npm run build
    npm run dev
