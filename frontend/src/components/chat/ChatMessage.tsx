import React, { useState } from 'react';
import { Bot, User, Copy, Check, RotateCcw, Sparkles, BookOpen } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '../../types';
import { CitationCard } from './CitationCard';
import { toast } from 'sonner';

interface ChatMessageProps {
  message: ChatMessageType;
  onRegenerate?: () => void;
  onOpenTimestamp?: (timestamp: number) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onRegenerate,
  onOpenTimestamp,
}) => {
  const [copied, setCopied] = useState(false);
  const isAI = message.sender === 'ai';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setCopied(true);
    toast.success('Response copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex gap-4 p-4 rounded-2xl transition-colors ${isAI ? 'glass-panel border border-white/5' : 'bg-slate-900/40 border border-slate-800'}`}>
      {/* Avatar Icon */}
      <div
        className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 text-white shadow-md ${
          isAI
            ? 'bg-gradient-to-tr from-brand-600 via-indigo-500 to-cyan-400 ring-2 ring-brand-500/30'
            : 'bg-slate-800 ring-2 ring-slate-700'
        }`}
      >
        {isAI ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5 text-slate-300" />}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-200">{isAI ? 'MVRAG Assistant' : 'You'}</span>
            <span className="text-[10px] text-slate-500 font-mono">{message.timestamp}</span>
          </div>

          {/* Message Actions */}
          <div className="flex items-center gap-1">
            <button
              onClick={handleCopy}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              title="Copy message"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
            {isAI && onRegenerate && (
              <button
                onClick={onRegenerate}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title="Regenerate answer"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Text Body */}
        <div className="text-xs text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">
          {message.text}
        </div>

        {/* Sources / Citations */}
        {isAI && message.sources && message.sources.length > 0 && (
          <div className="pt-3 border-t border-white/5 space-y-2">
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-brand-300">
              <BookOpen className="w-3.5 h-3.5 text-brand-400" />
              <span>ChromaDB Vector Citations ({message.sources.length})</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {message.sources.map((chunk, idx) => (
                <CitationCard key={idx} chunk={chunk} onOpenTimestamp={onOpenTimestamp} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
