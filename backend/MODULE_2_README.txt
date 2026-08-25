MVRAG MODULE 2 — BACKEND INTEGRATION

This module connects the existing frontend to the existing backend without
changing the working frame/Whisper/OCR/BLIP extraction algorithms.

FIXES INCLUDED
1. Adds GET /media/videos/{filename} for browser video playback.
2. QueryRequest accepts video_id.
3. Retrieval filters ChromaDB by video_id.
4. Chroma results preserve metadata, distances, and embedding IDs.
5. Reranker returns a stable 0..1 relevance score.
6. VideoPipeline stores video_id in new Chroma metadata.
7. BackgroundService passes db + video_id into VideoPipeline.
8. Pipeline persists transcripts, OCR, captions, chunks, and analytics
   in the existing SQLAlchemy tables.
9. GET /videos/{video_id} now returns the real persisted multimodal details.
10. Reprocessing removes existing Chroma vectors for that video when those
    vectors were created with video_id metadata.

IMPORTANT
- Do NOT delete the existing backend.
- Do NOT change the frame extraction interval or AI models in this module.
- Existing Chroma vectors created BEFORE this module do not contain video_id.
  They cannot be safely filtered by video. Reprocess each existing video once
  after installing this module so its vectors are rebuilt with video_id metadata.
- The existing SQL database is reused; no new table is introduced by Module 2.

INSTALL
From PowerShell:

cd D:\MVRAG\backend

Copy the contents of this module's src folder into:
D:\MVRAG\backend\src

Replace the existing files when prompted.

VALIDATE BEFORE STARTING
python -m compileall -q src

Then:
python -m uvicorn main:app --reload

EXPECTED ROUTES
GET  /media/videos/{filename}
GET  /videos/{video_id}
POST /query
POST /videos/upload

QUERY EXAMPLE
{
  "question": "Explain explicit typecasting.",
  "video_id": 16
}

VIDEO DETAILS
GET /videos/16 now includes:
- transcripts
- ocr_results
- captions
- chunks
- processing_stats

TEST VIDEO MEDIA
Open in browser:
http://127.0.0.1:8000/media/videos/<filename>

REPROCESSING
After Module 2 is installed, reprocess existing videos once.
This is necessary because their old Chroma vectors were indexed before
video_id was stored in metadata.

GIT
After validation:
git add .
git commit -m "Integrate backend video media and scoped RAG retrieval"
git push origin main
