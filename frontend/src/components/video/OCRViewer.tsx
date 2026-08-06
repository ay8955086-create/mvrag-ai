import React from 'react';
import { FileText, Clock, Sparkles } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';

interface OCRItem {
  id: number;
  frame_number: number;
  timestamp: number;
  text: string;
  confidence: number;
}

interface OCRViewerProps {
  ocrResults?: OCRItem[];
  onTimestampClick?: (timestamp: number) => void;
}

export const OCRViewer: React.FC<OCRViewerProps> = ({
  ocrResults = [],
  onTimestampClick,
}) => {
  return (
    <div className="space-y-3 max-h-[450px] overflow-y-auto pr-1">
      {ocrResults.length === 0 ? (
        <div className="text-center py-12 text-slate-500 text-xs">
          No OCR text detected in video frames.
        </div>
      ) : (
        ocrResults.map((ocr) => (
          <div
            key={ocr.id}
            className="p-3.5 rounded-xl bg-slate-900/40 border border-white/5 hover:border-slate-700 transition-colors flex items-start gap-3"
          >
            <button
              onClick={() => onTimestampClick && onTimestampClick(ocr.timestamp)}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[11px] font-mono font-semibold transition-colors flex-shrink-0"
            >
              <Clock className="w-3 h-3 text-indigo-400" />
              <span>{formatDuration(ocr.timestamp)}</span>
            </button>

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between text-[10px] text-slate-500 mb-1">
                <span>Frame #{ocr.frame_number}</span>
                <span className="text-emerald-400 font-mono">
                  Confidence: {Math.round(ocr.confidence * 100)}%
                </span>
              </div>
              <p className="text-xs text-slate-200 font-mono bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 break-words">
                {ocr.text}
              </p>
            </div>
          </div>
        ))
      )}
    </div>
  );
};
