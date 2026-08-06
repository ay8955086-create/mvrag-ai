import React from 'react';
import { Clock, ExternalLink, Sparkles, Layers } from 'lucide-react';
import { ContextChunk } from '../../types';
import { formatDuration } from '../../utils/formatters';

interface CitationCardProps {
  chunk: ContextChunk;
  onOpenTimestamp?: (timestamp: number) => void;
}

export const CitationCard: React.FC<CitationCardProps> = ({
  chunk,
  onOpenTimestamp,
}) => {
  const similarityPercent = Math.round((chunk.score || 0.85) * 100);
  const startTime = chunk.start_time || 0;

  return (
    <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-brand-500/40 transition-all duration-200 text-xs group">
      <div className="flex items-center justify-between gap-2 mb-2">
        <button
          onClick={() => onOpenTimestamp && onOpenTimestamp(startTime)}
          className="flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-brand-500/10 hover:bg-brand-500/20 text-brand-300 border border-brand-500/30 font-mono text-[10px] font-bold transition-colors"
        >
          <Clock className="w-3 h-3 text-brand-400" />
          <span>Jump to {formatDuration(startTime)}</span>
          <ExternalLink className="w-2.5 h-2.5 opacity-60" />
        </button>

        <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-mono font-semibold">
          <Sparkles className="w-3 h-3" />
          <span>{similarityPercent}% Match</span>
        </div>
      </div>

      <p className="text-slate-300 text-[11px] leading-relaxed line-clamp-3 italic">
        "{chunk.document}"
      </p>
    </div>
  );
};
