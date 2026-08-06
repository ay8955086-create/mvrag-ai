import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Sparkles, Loader2, Video, RefreshCw } from 'lucide-react';
import { useQueryRAG } from '../../hooks/useQueryRAG';
import { ChatMessage as ChatMessageType, VideoResponse } from '../../types';
import { ChatMessage } from './ChatMessage';
import { SuggestedQuestions } from './SuggestedQuestions';
import { Button } from '../ui/Button';

interface ChatContainerProps {
  videos?: VideoResponse[];
  selectedVideoId?: number | null;
  onSelectVideo?: (id: number | null) => void;
  onOpenTimestamp?: (timestamp: number) => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({
  videos = [],
  selectedVideoId,
  onSelectVideo,
  onOpenTimestamp,
}) => {
  const [questionInput, setQuestionInput] = useState('');
  const [messages, setMessages] = useState<ChatMessageType[]>([
    {
      id: 'welcome-msg',
      sender: 'ai',
      text: 'Hello! I am your MVRAG AI assistant. Ask me anything about your uploaded videos, transcripts, OCR screen text, or visual frame captions.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const bottomRef = useRef<HTMLDivElement>(null);
  const ragMutation = useQueryRAG();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, ragMutation.isPending]);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || questionInput.trim();
    if (!query || ragMutation.isPending) return;

    const userMsg: ChatMessageType = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setQuestionInput('');

    ragMutation.mutate(query, {
      onSuccess: (data) => {
        const aiMsg: ChatMessageType = {
          id: `ai-${Date.now()}`,
          sender: 'ai',
          text: data.answer || 'Based on the retrieved video segments, here is the answer to your question.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          sources: data.context || [],
        };
        setMessages((prev) => [...prev, aiMsg]);
      },
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8.5rem)] glass-card rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
      {/* Header Scope Bar */}
      <div className="p-4 bg-slate-900/80 border-b border-white/10 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              Multimodal RAG Assistant
              <span className="px-2 py-0.5 text-[9px] font-bold rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 uppercase">
                ChromaDB Hybrid
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Ask questions with auto vector retrieval & timestamp citations</p>
          </div>
        </div>

        {/* Video scope filter dropdown */}
        {videos.length > 0 && (
          <div className="flex items-center gap-2">
            <Video className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedVideoId || ''}
              onChange={(e) => onSelectVideo && onSelectVideo(e.target.value ? Number(e.target.value) : null)}
              className="bg-slate-950/80 border border-slate-700/80 text-slate-200 text-xs rounded-xl px-3 py-1.5 outline-none focus:border-brand-500"
            >
              <option value="">All Videos Scope ({videos.length})</option>
              {videos.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.title}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            message={msg}
            onRegenerate={() => handleSend(msg.text)}
            onOpenTimestamp={onOpenTimestamp}
          />
        ))}

        {/* Pending typing indicator */}
        {ragMutation.isPending && (
          <div className="flex items-center gap-3 p-4 rounded-2xl glass-panel border border-brand-500/30 text-xs text-brand-300 animate-pulse">
            <Loader2 className="w-4 h-4 animate-spin text-brand-400" />
            <span>Querying ChromaDB vector index & executing RAG pipeline...</span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-slate-950/90 border-t border-white/10 space-y-3">
        {messages.length < 3 && (
          <SuggestedQuestions onSelect={(q) => handleSend(q)} />
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative flex items-center gap-2"
        >
          <input
            type="text"
            value={questionInput}
            onChange={(e) => setQuestionInput(e.target.value)}
            placeholder="Ask a question about your videos (e.g. 'Explain explicit typecasting')..."
            className="w-full pl-4 pr-12 py-3 bg-slate-900/80 border border-slate-700/80 rounded-xl text-xs text-slate-100 placeholder-slate-500 outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all"
          />
          <Button
            type="submit"
            disabled={!questionInput.trim() || ragMutation.isPending}
            isLoading={ragMutation.isPending}
            size="sm"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg"
          >
            <Send className="w-3.5 h-3.5" />
          </Button>
        </form>
      </div>
    </div>
  );
};
