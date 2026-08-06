import React from 'react';
import { Image, Clock, Sparkles, Eye } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';

interface CaptionItem {
  id: number;
  frame_number: number;
  timestamp: number;
  caption: string;
}

interface FrameGalleryProps {
  captions?: CaptionItem[];
  onTimestampClick?: (timestamp: number) => void;
}

export const FrameGallery: React.FC<FrameGalleryProps> = ({
  captions = [],
  onTimestampClick,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[450px] overflow-y-auto pr-1">
      {captions.length === 0 ? (
        <div className="col-span-2 text-center py-12 text-slate-500 text-xs">
          No keyframe captions available.
        </div>
      ) : (
        captions.map((item) => (
          <div
            key={item.id}
            className="group glass-card rounded-xl overflow-hidden border border-white/5 hover:border-brand-500/40 transition-all duration-300"
          >
            {/* Visual keyframe mockup */}
            <div className="relative aspect-video bg-slate-950 flex items-center justify-center overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-tr from-slate-950 via-slate-900 to-indigo-950/40 flex flex-col items-center justify-center p-4 text-center">
                <Image className="w-8 h-8 text-indigo-400/60 mb-2 group-hover:scale-110 transition-transform" />
                <span className="text-[10px] text-slate-500 font-mono">Frame #{item.frame_number}</span>
              </div>
              <button
                onClick={() => onTimestampClick && onTimestampClick(item.timestamp)}
                className="absolute top-2 left-2 z-10 px-2 py-0.5 rounded-md bg-slate-950/80 backdrop-blur-md text-[10px] font-mono text-brand-300 border border-brand-500/30 flex items-center gap-1 hover:bg-brand-600 hover:text-white transition-colors"
              >
                <Clock className="w-2.5 h-2.5" />
                <span>{formatDuration(item.timestamp)}</span>
              </button>
            </div>

            {/* BLIP Caption */}
            <div className="p-3">
              <div className="flex items-center gap-1.5 text-[10px] text-brand-400 font-bold uppercase tracking-wider mb-1">
                <Sparkles className="w-3 h-3" />
                <span>BLIP Vision Caption</span>
              </div>
              <p className="text-xs text-slate-300 leading-snug">
                "{item.caption}"
              </p>
            </div>
          </div>
        ))
      )}
    </div>
  );
};
