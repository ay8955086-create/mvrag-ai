import React, { useState } from 'react';
import { Search, Clock, Mic, Copy, Check } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';
import { toast } from 'sonner';

interface TranscriptSegment {
  id: number;
  start_time: number;
  end_time: number;
  text: string;
  language?: string;
  confidence?: number;
}

interface TranscriptViewerProps {
  segments?: TranscriptSegment[];
  onTimestampClick?: (timestamp: number) => void;
}

export const TranscriptViewer: React.FC<TranscriptViewerProps> = ({
  segments = [],
  onTimestampClick,
}) => {
  const [filterText, setFilterText] = useState('');
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const filteredSegments = segments.filter((s) =>
    s.text.toLowerCase().includes(filterText.toLowerCase())
  );

  const handleCopy = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    toast.success('Transcript snippet copied to clipboard');
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="space-y-4">
      {/* Search Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            placeholder="Search transcript text..."
            className="w-full pl-10 pr-4 py-2 bg-slate-900/60 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 outline-none focus:border-brand-500"
          />
        </div>
        <span className="text-xs text-slate-400 font-mono">
          {filteredSegments.length} segments
        </span>
      </div>

      {/* Segments Timeline */}
      <div className="space-y-2 max-h-[450px] overflow-y-auto pr-1">
        {filteredSegments.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-xs">
            No matching transcript segments found.
          </div>
        ) : (
          filteredSegments.map((segment) => (
            <div
              key={segment.id}
              className="p-3 rounded-xl bg-slate-900/40 hover:bg-slate-900/80 border border-white/5 transition-colors group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3 flex-1">
                {/* Timestamp Pill */}
                <button
                  onClick={() => onTimestampClick && onTimestampClick(segment.start_time)}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-brand-500/10 hover:bg-brand-500/20 text-brand-300 border border-brand-500/30 text-[11px] font-mono font-semibold transition-colors flex-shrink-0"
                  title="Jump video to timestamp"
                >
                  <Clock className="w-3 h-3 text-brand-400" />
                  <span>{formatDuration(segment.start_time)}</span>
                </button>

                {/* Text Content */}
                <p className="text-xs text-slate-200 leading-relaxed pt-0.5">
                  {segment.text}
                </p>
              </div>

              <button
                onClick={() => handleCopy(segment.id, segment.text)}
                className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
                title="Copy snippet"
              >
                {copiedId === segment.id ? (
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                ) : (
                  <Copy className="w-3.5 h-3.5" />
                )}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
