# 🎥 MVRAG AI

<div align="center">

# Multimodal Video Retrieval-Augmented Generation

### Transform Videos into Searchable Intelligence

AI-powered Enterprise Video Intelligence Platform that allows users to chat with videos using Speech Recognition, OCR, Image Captioning, Vector Search, and Large Language Models.

</div>

---

# Overview

MVRAG AI is an enterprise-grade multimodal Retrieval-Augmented Generation (RAG) platform designed to understand videos instead of treating them as ordinary files.

The system extracts:

- 🎙 Speech (Whisper)
- 📝 OCR Text (EasyOCR)
- 🖼 Image Captions (BLIP-2)
- 📚 Semantic Embeddings
- ⏱ Video Metadata
- 🎯 Timestamps

All extracted information is indexed into a vector database, allowing users to ask natural language questions and receive context-aware answers with relevant timestamps.

---

# Features

- 🎥 Video Upload
- 🎙 Automatic Speech Transcription
- 📝 OCR from Video Frames
- 🖼 AI Image Captioning
- 📚 Semantic Chunking
- 🔎 Vector Search
- 🤖 GPT / Gemini / Ollama Support
- 📊 Analytics Dashboard
- 📑 AI Notes Generator
- ❓ Quiz Generator
- 📄 PDF Export
- 🌙 Dark Theme
- 📌 Timestamp Navigation

---

# System Architecture

```
                    Streamlit UI
                           │
                           ▼
                     FastAPI Backend
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     Video Engine      AI Pipeline     Vector Database
          │                │                │
          ▼                ▼                ▼
   FFmpeg/OpenCV   Whisper + OCR + BLIP   ChromaDB
                           │
                           ▼
                    Embedding Layer
                           │
                           ▼
                     Retrieval Engine
                           │
                           ▼
                     GPT / Gemini / Ollama
                           │
                           ▼
                      Final Response
```

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- SQLite

## Frontend

- Streamlit
- Plotly

## AI

- Whisper
- EasyOCR
- BLIP-2
- Sentence Transformers
- CLIP

## Retrieval

- ChromaDB
- BGE Embeddings
- BGE Reranker

## LLM

- OpenAI GPT
- Google Gemini
- Ollama

---

# Folder Structure

```text
MVRAG/
│
├── src/
├── data/
├── database/
├── vector_db/
├── configs/
├── docs/
├── logs/
├── tests/
├── tools/
├── requirements.txt
├── main.py
└── README.md
```

---

# Workflow

```
Upload Video

↓

Extract Audio

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

Question

↓

Retriever

↓

LLM

↓

Answer
```

---

# Installation

```bash
git clone <repository-url>

cd MVRAG
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run

```bash
python main.py
```

---

# Future Scope

- Live Video Processing
- Multi-user Authentication
- Cloud Deployment
- Distributed Vector Database
- Kubernetes Support
- Multi-GPU Inference
- Agentic Video Analysis

---

# License

MIT License

---

<div align="center">

Made with ❤️ using Python, FastAPI, Streamlit and AI

</div>