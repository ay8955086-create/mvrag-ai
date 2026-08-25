import React from 'react';
import { Clock, ExternalLink, Sparkles } from 'lucide-react';
import { ContextChunk } from '../../types';
import { formatDuration } from '../../utils/formatters';

interface CitationCardProps {
  chunk: ContextChunk;
  onOpenTimestamp?: (timestamp: number) => void;
}

const clampScore = (score: number) =>
  Math.max(0, Math.min(1, score));

export const CitationCard: React.FC<CitationCardProps> = ({
  chunk,
  onOpenTimestamp,
}) => {
  const score =
    typeof chunk.score === 'number' && Number.isFinite(chunk.score)
      ? clampScore(chunk.score)
      : null;

  const startTime =
    typeof chunk.start_time === 'number' && Number.isFinite(chunk.start_time)
      ? Math.max(0, chunk.start_time)
      : null;

  const sourceText =
    chunk.document?.trim() ||
    [chunk.transcript, chunk.ocr_text, chunk.caption]
      .filter((value): value is string => Boolean(value?.trim()))
      .join(' ');

  return (
    <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-brand-500/40 transition-all duration-200 text-xs group">
      <div className="flex items-center justify-between gap-2 mb-2">
        {startTime !== null ? (
          <button
            onClick={() => onOpenTimestamp?.(startTime)}
            className="flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-brand-500/10 hover:bg-brand-500/20 text-brand-300 border border-brand-500/30 font-mono text-[10px] font-bold transition-colors"
          >
            <Clock className="w-3 h-3 text-brand-400" />
            <span>Jump to {formatDuration(startTime)}</span>
            <ExternalLink className="w-2.5 h-2.5 opacity-60" />
          </button>
        ) : (
          <span className="text-[10px] text-slate-500">
            Timestamp unavailable
          </span>
        )}

        {score !== null ? (
          <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-mono font-semibold">
            <Sparkles className="w-3 h-3" />
            <span>{Math.round(score * 100)}% Match</span>
          </div>
        ) : (
          <span className="text-[10px] text-slate-500 font-mono">
            Score unavailable
          </span>
        )}
      </div>

      <p className="text-slate-300 text-[11px] leading-relaxed line-clamp-4 italic">
        {sourceText ? `"${sourceText}"` : 'No source text returned.'}
      </p>
    </div>
  );
};
