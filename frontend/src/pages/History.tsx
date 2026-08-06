import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { History as HistoryIcon, Search, Bot, Clock, ExternalLink, Trash2, ArrowRight } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { toast } from 'sonner';

interface HistoryItem {
  id: string;
  question: string;
  answer: string;
  timestamp: string;
  sourcesCount: number;
}

export const History: React.FC = () => {
  const navigate = useNavigate();

  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([
    {
      id: 'h1',
      question: 'Explain explicit typecasting from the video.',
      answer: 'Explicit typecasting in C++ converts a variable from one data type to another using casting operators like static_cast or standard functional cast expressions.',
      timestamp: '2026-08-06 14:10',
      sourcesCount: 3,
    },
    {
      id: 'h2',
      question: 'What OCR text was detected on the main slide?',
      answer: 'Detected screen text includes "[Class MVRAG Pipeline Step 1] Code block / Slide Title: Explicit Typecasting Demo".',
      timestamp: '2026-08-06 13:45',
      sourcesCount: 2,
    },
    {
      id: 'h3',
      question: 'Summarize the core topics covered in the session.',
      answer: 'The session covers audio extraction, Whisper transcription, OCR frame detection, BLIP visual captioning, and ChromaDB vector retrieval.',
      timestamp: '2026-08-06 12:30',
      sourcesCount: 4,
    },
  ]);

  const [filterQuery, setFilterQuery] = useState('');

  const filtered = historyItems.filter(
    (h) =>
      h.question.toLowerCase().includes(filterQuery.toLowerCase()) ||
      h.answer.toLowerCase().includes(filterQuery.toLowerCase())
  );

  const handleClearHistory = () => {
    setHistoryItems([]);
    toast.success('Query history cleared.');
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
            <HistoryIcon className="w-6 h-6 text-brand-400" />
            RAG Query History
          </h1>
          <p className="text-xs text-slate-400">
            Review past questions asked over indexed videos, AI answers, and vector citation sources.
          </p>
        </div>

        {historyItems.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={handleClearHistory}
            leftIcon={<Trash2 className="w-3.5 h-3.5 text-rose-400" />}
          >
            Clear History
          </Button>
        )}
      </div>

      {/* Filter Bar */}
      <div className="relative max-w-md">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <input
          type="text"
          value={filterQuery}
          onChange={(e) => setFilterQuery(e.target.value)}
          placeholder="Filter history by question or answer keywords..."
          className="w-full pl-10 pr-4 py-2 bg-slate-900/80 border border-slate-700/80 rounded-xl text-xs text-slate-100 placeholder-slate-500 outline-none focus:border-brand-500"
        />
      </div>

      {/* History Items List */}
      {filtered.length === 0 ? (
        <Card glass className="p-12 text-center space-y-4">
          <HistoryIcon className="w-8 h-8 text-slate-500 mx-auto" />
          <h3 className="text-sm font-bold text-slate-200">No Query History Found</h3>
          <p className="text-xs text-slate-400">Ask questions in the AI Chat to populate your query log.</p>
          <Button size="sm" onClick={() => navigate('/chat')}>Open AI Chat</Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {filtered.map((item) => (
            <Card key={item.id} hoverGlow className="p-5 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-mono text-slate-400 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  {item.timestamp}
                </span>
                <span className="px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-300 border border-brand-500/20 text-[10px] font-mono font-bold">
                  {item.sourcesCount} Citations
                </span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <Bot className="w-4 h-4 text-brand-400" />
                  Q: {item.question}
                </h3>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed bg-slate-950/40 p-3 rounded-xl border border-white/5">
                  {item.answer}
                </p>
              </div>

              <div className="flex justify-end pt-2">
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => navigate(`/search?q=${encodeURIComponent(item.question)}`)}
                  rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
                  className="text-xs text-brand-300"
                >
                  Re-run Query
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
