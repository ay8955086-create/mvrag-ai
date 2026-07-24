# MVRAG AI Database Schema

## Database

- Engine: SQLite
- ORM: SQLAlchemy 2.x

---

# Entity Relationship Diagram

```
Video
│
├── Transcript
├── OCR
├── Caption
├── Chunk
│      │
│      └── Embedding (Vector DB)
│
├── Query
│
└── Analytics
```

---

# Tables

## 1. videos

Stores uploaded video information.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary Key |
| filename | String | Original filename |
| title | String | Display title |
| description | Text | Optional description |
| duration | Float | Seconds |
| fps | Float | Frames per second |
| width | Integer | Resolution width |
| height | Integer | Resolution height |
| size_mb | Float | File size |
| status | String | Processing status |
| upload_time | DateTime | Upload timestamp |
| processed_time | DateTime | Processing completion |
| created_at | DateTime | Record creation |
| updated_at | DateTime | Last update |

---

## 2. transcripts

Stores Whisper transcription.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| start_time | Float |
| end_time | Float |
| text | Text |
| language | String |
| confidence | Float |

---

## 3. ocr_results

Stores OCR text extracted from frames.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| frame_number | Integer |
| timestamp | Float |
| text | Text |
| confidence | Float |

---

## 4. captions

Stores BLIP-generated image captions.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| frame_number | Integer |
| timestamp | Float |
| caption | Text |

---

## 5. chunks

Semantic chunks used for RAG.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| start_time | Float |
| end_time | Float |
| transcript | Text |
| ocr_text | Text |
| caption | Text |
| embedding_id | String |

---

## 6. queries

Stores user questions.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| question | Text |
| answer | Text |
| response_time | Float |
| created_at | DateTime |

---

## 7. analytics

Stores processing statistics.

| Column | Type |
|---------|------|
| id | UUID |
| video_id | UUID |
| processing_time | Float |
| transcript_count | Integer |
| ocr_count | Integer |
| caption_count | Integer |
| chunk_count | Integer |

---

# Relationships

Video

- has many Transcripts
- has many OCR Results
- has many Captions
- has many Chunks
- has many Queries
- has one Analytics record

Transcript

- belongs to Video

OCR

- belongs to Video

Caption

- belongs to Video

Chunk

- belongs to Video

Query

- belongs to Video

Analytics

- belongs to Video

---

# Deletion Policy

Deleting a Video should automatically delete:

- Transcript
- OCR Results
- Captions
- Chunks
- Queries
- Analytics

(CASCADE DELETE)

---

# Vector Database

Embeddings are **not stored in SQLite**.

SQLite stores only:

- embedding_id

Actual vectors are stored in ChromaDB.

---

# Primary Keys

Every table uses UUID as the primary key.

---

# Indexes

Create indexes on:

- video_id
- upload_time
- status
- created_at

---

# Future Expansion

The schema is designed to support:

- Multiple users
- Authentication
- Team workspaces
- Cloud storage
- Multiple vector databases
- Distributed processing
- PostgreSQL migration