import React, { useEffect, useRef, useState } from 'react';
import { Film } from 'lucide-react';
import { getVideoMediaUrl } from '../../services/api';

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
  const [hasError, setHasError] = useState(false);

  const videoUrl = getVideoMediaUrl(filename);

  useEffect(() => {
    setHasError(false);
  }, [videoUrl]);

  useEffect(() => {
    const video = videoRef.current;

    if (
      video &&
      seekTimestamp !== undefined &&
      seekTimestamp !== null &&
      Number.isFinite(seekTimestamp)
    ) {
      video.currentTime = Math.max(0, seekTimestamp);
      void video.play().catch(() => {
        // Autoplay can be blocked; seeking still works.
      });
    }
  }, [seekTimestamp]);

  return (
    <div className="relative rounded-2xl overflow-hidden glass-panel border border-white/10 shadow-2xl bg-black group">
      <video
        ref={videoRef}
        controls
        preload="metadata"
        playsInline
        className="w-full aspect-video object-contain bg-black"
        onLoadedMetadata={() => setHasError(false)}
        onError={() => setHasError(true)}
        onTimeUpdate={(event) => {
          onTimeUpdate?.(event.currentTarget.currentTime);
        }}
      >
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support video playback.
      </video>

      <div className="p-3 bg-slate-950/80 backdrop-blur-md border-t border-white/10 flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 min-w-0">
          <Film className="w-4 h-4 text-brand-400 shrink-0" />
          <span className="font-semibold text-slate-200 truncate">
            {title}
          </span>
        </div>

        {hasError ? (
          <span className="text-rose-400 shrink-0">
            Unable to load video
          </span>
        ) : (
          <span className="font-mono text-[11px] text-slate-500 truncate">
            Video stream
          </span>
        )}
      </div>
    </div>
  );
};
