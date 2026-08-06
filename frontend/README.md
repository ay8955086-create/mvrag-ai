# MVRAG AI - Multimodal Video RAG Frontend

Production-ready, high-performance React 19 + TypeScript + Vite + TailwindCSS frontend application for **MVRAG AI** (Multimodal Video Retrieval-Augmented Generation).

Designed with glassmorphism, modern AI SaaS aesthetics (Apple, OpenAI, Linear.app, Cursor IDE feel), responsive layouts, and interactive telemetry dashboards.

---

## 🛠️ Tech Stack

- **Framework**: React 19 + Vite
- **Language**: TypeScript
- **Styling**: TailwindCSS + Glassmorphism
- **Animations**: Framer Motion
- **Data Fetching**: @tanstack/react-query + Axios
- **Charts**: Recharts
- **Icons**: Lucide Icons
- **Toast Notifications**: Sonner
- **Form Validation**: React Hook Form + Zod

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Run Development Server
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🗺️ Page Routes & Features

1. **Login** (`/login`) - Secure user sign in.
2. **Register** (`/register`) - Account creation.
3. **Dashboard** (`/`) - System stats, hero banner, quick actions, recent activity feed.
4. **Upload Video** (`/upload`) - Drag & drop uploader with file validation & upload progress tracking.
5. **Processing Status** (`/processing/:id`) - Real-time animated step timeline of video ingestion stages.
6. **Video Library** (`/videos`) - Repository of all videos with search, status filters, sorting & deletion.
7. **Video Details** (`/videos/:id`) - Video player with timestamp seeking, Whisper transcripts, OCR text, BLIP frame captions & ChromaDB chunk inspector.
8. **AI Chat** (`/chat`) - ChatGPT-style RAG conversational assistant with vector citation cards and timestamp deep links.
9. **Semantic Search** (`/search`) - Hybrid vector search across speech, OCR text, and visual captions.
10. **Analytics** (`/analytics`) - Recharts volume & storage allocation charts.
11. **Query History** (`/history`) - History log of past RAG queries and synthesized answers.
12. **Settings** (`/settings`) - Dark/Light mode toggle, FastAPI URL, LLM engine selection.
13. **User Profile** (`/profile`) - User information & developer REST API key.
14. **About** (`/about`) - MVRAG architecture & tech stack breakdown.
15. **Error Pages** (`*`) - Custom 404 page.

---

## 🔌 FastAPI Backend Integration

The frontend seamlessly connects to the FastAPI backend running at `http://localhost:8000`:

- `POST /videos/upload` - Upload video file with title & description
- `GET /videos` - List all uploaded videos
- `GET /videos/{id}` - Get video metadata
- `DELETE /videos/{id}` - Delete video record and local storage
- `POST /query` - Execute multimodal vector retrieval & RAG question answering
- `GET /analytics` - Get aggregate system metrics
