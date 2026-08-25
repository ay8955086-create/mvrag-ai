import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Search as SearchIcon, Sparkles, Clock, ExternalLink, Layers, Bot, Film } from 'lucide-react';
import { useQueryRAG } from '../hooks/useQueryRAG';
import { useVideos } from '../hooks/useVideos';
import { ContextChunk } from '../types';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { formatDuration } from '../utils/formatters';

export const Search: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  const navigate = useNavigate();

  const [queryInput, setQueryInput] = useState(initialQuery);
  const ragMutation = useQueryRAG();
  const { data: videos } = useVideos();

  useEffect(() => {
    if (initialQuery) {
      ragMutation.mutate({ question: initialQuery });
    }
  }, [initialQuery]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (queryInput.trim()) {
      ragMutation.mutate({ question: queryInput.trim() });
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-8">
      {/* Search Bar Header */}
      <div className="text-center space-y-4 py-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 text-brand-300 border border-brand-500/30 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Multimodal Hybrid Vector Search</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-100 tracking-tight">
          Semantic Video Search Engine
        </h1>
        <p className="text-xs text-slate-400 max-w-lg mx-auto">
          Query across acoustic Whisper transcripts, OCR screen text, and BLIP vision frame captions indexed in ChromaDB.
        </p>

        <form onSubmit={handleSearchSubmit} className="relative max-w-2xl mx-auto flex items-center gap-2">
          <div className="relative flex-1">
            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              value={queryInput}
              onChange={(e) => setQueryInput(e.target.value)}
              placeholder="Search concepts, code, or spoken topics (e.g. 'typecasting')..."
              className="w-full pl-12 pr-4 py-3.5 bg-slate-900/80 border border-slate-700/80 rounded-2xl text-sm text-slate-100 placeholder-slate-500 outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 shadow-xl transition-all"
            />
          </div>
          <Button
            type="submit"
            isLoading={ragMutation.isPending}
            disabled={!queryInput.trim() || ragMutation.isPending}
            className="px-6 py-3.5 rounded-2xl shadow-xl shadow-brand-500/25"
          >
            Search
          </Button>
        </form>
      </div>

      {/* Results Section */}
      {ragMutation.isPending && (
        <Card glass className="p-12 text-center space-y-3">
          <Sparkles className="w-8 h-8 text-brand-400 animate-spin mx-auto" />
          <h3 className="text-sm font-bold text-slate-200">Executing Vector Search & BGE Reranker...</h3>
          <p className="text-xs text-slate-400">Comparing dense embeddings in ChromaDB collection.</p>
        </Card>
      )}

      {ragMutation.isSuccess && ragMutation.data && (
        <div className="space-y-6">
          {/* AI Generated Overview Answer */}
          <Card glass className="p-6 space-y-3 border-brand-500/30">
            <div className="flex items-center gap-2 text-xs font-bold text-brand-300">
              <Bot className="w-4 h-4 text-brand-400" />
              <span>AI Synthesized Answer Overview</span>
            </div>
            <p className="text-xs text-slate-200 leading-relaxed font-sans bg-slate-950/40 p-4 rounded-xl border border-white/5">
              {ragMutation.data.answer}
            </p>
          </Card>

          {/* Context Snippet Cards */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-200">
              Top Relevant Video Snippets ({ragMutation.data.context.length})
            </h3>

            <div className="grid grid-cols-1 gap-4">
              {ragMutation.data.context.map((chunk: ContextChunk, idx: number) => {
                const matchedVideo = chunk.video_id
                  ? videos?.find((video) => video.id === chunk.video_id)
                  : undefined;
                const scorePercent =
                  typeof chunk.score === 'number' && Number.isFinite(chunk.score)
                    ? Math.round(Math.max(0, Math.min(1, chunk.score)) * 100)
                    : null;

                return (
                  <Card key={idx} hoverGlow className="p-5 flex flex-col md:flex-row items-start justify-between gap-4">
                    <div className="space-y-2 flex-1">
                      <div className="flex items-center gap-2 text-xs">
                        <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono text-[10px] font-bold">
                          {scorePercent !== null ? `${scorePercent}% Similarity Score` : 'Similarity unavailable'}
                        </span>
                        <span className="font-mono text-slate-400 text-[10px]">Snippet #{idx + 1}</span>
                      </div>

                      <p className="text-xs text-slate-200 leading-relaxed bg-slate-950/60 p-3 rounded-xl border border-slate-800 font-mono">
                        "{chunk.document}"
                      </p>
                    </div>

                    <div className="flex flex-col items-end gap-2 flex-shrink-0">
                      {matchedVideo && (
                        <Button
                          size="sm"
                          onClick={() => navigate(`/videos/${matchedVideo.id}`)}
                          leftIcon={<Clock className="w-3.5 h-3.5" />}
                          rightIcon={<ExternalLink className="w-3.5 h-3.5" />}
                        >
                          Open Timestamp
                        </Button>
                      )}
                    </div>
                  </Card>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
