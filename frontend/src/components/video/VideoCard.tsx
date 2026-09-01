import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Play,
  Trash2,
  Clock,
  HardDrive,
  Calendar,
  Layers,
  Sparkles,
  ExternalLink,
  MessageSquare,
} from 'lucide-react';
import { VideoResponse } from '../../types';
import { formatDuration, formatFileSize, formatDate, getStatusBadgeClass } from '../../utils/formatters';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';

interface VideoCardProps {
  video: VideoResponse;
  onDelete: (id: number) => void;
}

export const VideoCard: React.FC<VideoCardProps> = ({ video, onDelete }) => {
  const navigate = useNavigate();

  return (
    <Card hoverGlow className="group relative flex flex-col justify-between h-full">
      {/* Video Thumbnail Overlay */}
      <div className="relative aspect-video w-full bg-slate-950 overflow-hidden">
        {/* Mock visual preview backdrop */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/40 via-slate-900 to-slate-950 flex items-center justify-center">
          <Layers className="w-12 h-12 text-slate-700/60 group-hover:scale-110 transition-transform duration-300" />
        </div>

        {/* Status Badge */}
        <div className="absolute top-3 left-3 z-10">
          <span className={`px-2.5 py-1 text-[10px] font-bold rounded-full border ${getStatusBadgeClass(video.status)} uppercase tracking-wider`}>
            {video.status}
          </span>
        </div>

        {/* Duration Badge */}
        <div className="absolute bottom-3 right-3 z-10 px-2 py-0.5 text-[11px] font-mono font-semibold text-slate-200 bg-slate-950/80 backdrop-blur-md rounded-md border border-white/10">
          {formatDuration(video.duration)}
        </div>

        {/* Play Overlay Button */}
        <div
          onClick={() => navigate(`/videos/${video.id}`)}
          className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 backdrop-blur-[2px] transition-all duration-300 flex items-center justify-center cursor-pointer"
        >
          <div className="w-12 h-12 rounded-full bg-brand-600/90 text-white flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
            <Play className="w-5 h-5 fill-current translate-x-0.5" />
          </div>
        </div>
      </div>

      {/* Card Info */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          <h3
            onClick={() => navigate(`/videos/${video.id}`)}
            className="text-sm font-bold text-slate-100 group-hover:text-brand-300 transition-colors line-clamp-1 cursor-pointer"
            title={video.title}
          >
            {video.title}
          </h3>
          <p className="text-xs text-slate-400 mt-1 line-clamp-2 min-h-[32px]">
            {video.description || 'No description provided.'}
          </p>
        </div>

        {/* Metadata Details */}
        <div className="mt-4 pt-3 border-t border-white/5 space-y-2 text-[11px] text-slate-400">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <HardDrive className="w-3.5 h-3.5 text-slate-500" />
              {formatFileSize(video.size_mb)}
            </span>
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-500" />
              {formatDate(video.upload_time)}
            </span>
          </div>

          <div className="flex items-center justify-between text-slate-500">
            <span>Resolution: {video.width || 1920}x{video.height || 1080}</span>
            <span>{video.fps || 30} FPS</span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="px-4 py-3 bg-slate-900/60 border-t border-white/5 flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5">

          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(`/videos/${video.id}`)}
            className="text-xs text-slate-300"
            leftIcon={<ExternalLink className="w-3.5 h-3.5" />}
          >
            Details
          </Button>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => onDelete(video.id)}
          className="text-slate-500 hover:text-rose-400 hover:bg-rose-500/10"
          title="Delete Video"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </Card>
  );
};
