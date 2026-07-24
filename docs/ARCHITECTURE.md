# MVRAG AI Architecture Document

**Project:** MVRAG AI  
**Full Form:** Multimodal Video Retrieval-Augmented Generation

---

# 1. Project Goal

MVRAG AI is an enterprise-grade multimodal video intelligence platform.

The system converts videos into searchable knowledge by combining:

- Speech Recognition
- OCR
- Image Captioning
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Large Language Models

Users can ask questions in natural language and receive:

- Answers
- Timestamps
- Transcript snippets
- OCR text
- Image descriptions
- Source references

---

# 2. High-Level Architecture

```
                    Streamlit UI
                          │
                          ▼
                    FastAPI Backend
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Upload Service      Query Service     Analytics Service
      │                   │                   │
      └──────────────┬────┴──────────────┬────┘
                     ▼                   ▼
              Pipeline Manager      Metadata Database
                     │
     ┌───────────────┼────────────────────────┐
     ▼               ▼                        ▼
Video Processing   AI Processing        Vector Database
     │               │                        │
     ▼               ▼                        ▼
 FFmpeg/OpenCV   Whisper/OCR/BLIP       ChromaDB
                     │
                     ▼
              Embedding Engine
                     │
                     ▼
              Hybrid Retriever
                     │
                     ▼
                 LLM Gateway
                     │
                     ▼
               Answer Generator
```

---

# 3. Folder Structure

```
MVRAG/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
│
├── configs/
│
├── data/
│   ├── raw_videos/
│   ├── audio/
│   ├── frames/
│   ├── keyframes/
│   ├── captions/
│   ├── transcripts/
│   ├── ocr/
│   ├── thumbnails/
│   ├── processed_chunks/
│   └── exports/
│
├── database/
├── docs/
├── logs/
├── tests/
├── tools/
├── vector_db/
│
└── src/
    ├── config/
    ├── core/
    ├── database/
    ├── models/
    ├── ingestion/
    ├── ai/
    ├── embeddings/
    ├── retrieval/
    ├── generation/
    ├── services/
    ├── pipelines/
    ├── api/
    ├── ui/
    └── utils/
```

---

# 4. Dependency Rules

Every dependency flows downward only.

```
settings
      │
      ▼
constants
      │
      ▼
exceptions
      │
      ▼
logger
      │
      ▼
database
      │
      ▼
services
      │
      ▼
pipelines
      │
      ▼
api
      │
      ▼
ui
```

No circular imports.

---

# 5. AI Pipeline

```
Video

↓

Audio Extraction

↓

Speech Recognition

↓

Frame Extraction

↓

OCR

↓

Caption Generation

↓

Chunking

↓

Embeddings

↓

Vector Database

↓

Retriever

↓

Reranker

↓

Prompt Builder

↓

LLM

↓

Answer
```

---

# 6. Backend Responsibilities

## Config
- Environment
- Paths
- Settings

## Core
- Constants
- Exceptions
- Logging

## Database
- SQLite
- ORM
- Metadata

## Ingestion
- Video loading
- Audio extraction
- Frame extraction

## AI
- Whisper
- EasyOCR
- BLIP

## Embeddings
- Text
- Image
- Fusion

## Retrieval
- ChromaDB
- Retriever
- Reranker

## Generation
- Prompt Builder
- LLM Gateway
- Answer Generator

## Services
Business logic only.

## Pipelines
Workflow orchestration.

## API
FastAPI routes.

## UI
Streamlit pages.

---

# 7. Coding Standards

- Python 3.11
- Type hints
- Google-style docstrings
- pathlib instead of os.path
- No print() in production
- Logging everywhere
- No hardcoded paths
- No global mutable state
- Dependency Injection where appropriate

---

# 8. Logging Strategy

Every module obtains a logger from the central logger manager.

No module configures logging independently.

---

# 9. Error Handling

All custom exceptions inherit from:

```
MVRAGException
```

No bare `except:` blocks.

---

# 10. Database

SQLite

Stores:

- Video metadata
- Processing status
- User queries
- Analytics

Vector embeddings are stored in ChromaDB.

---

# 11. API Endpoints

```
POST /upload

GET /videos

GET /video/{id}

POST /query

GET /analytics

GET /health
```

---

# 12. Streamlit Pages

- Dashboard
- Upload
- Library
- Chat
- Analytics
- Settings

---

# 13. Development Order

1. settings.py
2. constants.py
3. exceptions.py
4. logger.py
5. main.py
6. database
7. models
8. ingestion
9. ai
10. embeddings
11. retrieval
12. generation
13. services
14. pipelines
15. api
16. ui
17. tests

---

# 14. Definition of Done

A file is considered complete when:

- It passes formatting.
- It includes type hints.
- It includes documentation.
- It has no placeholder code.
- It requires no redesign because of architecture.

Bug fixes are acceptable; architectural rewrites are not.
