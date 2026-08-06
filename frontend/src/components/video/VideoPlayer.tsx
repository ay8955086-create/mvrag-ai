import React, { useRef, useEffect } from 'react';
import { Play, Pause, Volume2, Maximize, Film } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';

interface VideoPlayerProps {
  filename: string;
  title: string;
  seekTimestamp?: number | null;
  onTimeUpdate?: (currentTime: number) => void;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({
  filename,
  title,
  seekTimestamp,
  onTimeUpdate,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (seekTimestamp !== undefined && seekTimestamp !== null && videoRef.current) {
      videoRef.current.currentTime = seekTimestamp;
      videoRef.current.play().catch(() => {});
    }
  }, [seekTimestamp]);

  const videoUrl = `/api/data/raw_videos/${filename}`;

  return (
    <div className="relative rounded-2xl overflow-hidden glass-panel border border-white/10 shadow-2xl bg-black group">
      {/* Video Element */}
      <video
        ref={videoRef}
        controls
        preload="metadata"
        className="w-full aspect-video object-contain bg-black"
        onTimeUpdate={(e) => {
          if (onTimeUpdate) {
            onTimeUpdate(e.currentTarget.currentTime);
          }
        }}
      >
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support video playback.
      </video>

      {/* Fallback Overlay if video fails to load directly from local dev */}
      <div className="p-3 bg-slate-950/80 backdrop-blur-md border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <Film className="w-4 h-4 text-brand-400" />
          <span className="font-semibold text-slate-200 truncate">{title}</span>
        </div>
        <span className="font-mono text-[11px] text-slate-400">Source: raw_videos/{filename}</span>
      </div>
    </div>
  );
};
