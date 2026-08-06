import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Activity, CheckCircle2, ArrowRight, Bot, ExternalLink, RefreshCw } from 'lucide-react';
import { useVideo } from '../hooks/useVideos';
import { PipelineTimeline } from '../components/pipeline/PipelineTimeline';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Skeleton } from '../components/ui/Skeleton';
import { getStatusBadgeClass, formatFileSize, formatDuration } from '../utils/formatters';

export const ProcessingStatus: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const videoId = Number(id);
  const navigate = useNavigate();

  const { data: video, isLoading, isError, refetch } = useVideo(videoId);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <Skeleton className="h-40 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (isError || !video) {
    return (
      <Card glass className="max-w-xl mx-auto p-8 text-center space-y-4">
        <h2 className="text-lg font-bold text-rose-400">Video Not Found</h2>
        <p className="text-xs text-slate-400">Could not retrieve processing status for Video ID #{id}.</p>
        <Button onClick={() => navigate('/videos')}>Return to Video Library</Button>
      </Card>
    );
  }

  const isCompleted = video.status === 'Completed';

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-8">
      {/* Top Banner */}
      <Card glass className="p-6">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full border ${getStatusBadgeClass(video.status)} uppercase`}>
                {video.status}
              </span>
              <span className="text-xs font-mono text-slate-400">ID: #{video.id}</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">{video.title}</h1>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Duration: {formatDuration(video.duration)} | Size: {formatFileSize(video.size_mb)} | File: {video.filename}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => refetch()}
              leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
            >
              Refresh Status
            </Button>
            {isCompleted && (
              <Button
                size="sm"
                onClick={() => navigate(`/chat?videoId=${video.id}`)}
                leftIcon={<Bot className="w-4 h-4 text-white" />}
                className="shadow-lg shadow-brand-500/20"
              >
                Ask AI Questions
              </Button>
            )}
          </div>
        </div>
      </Card>

      {/* Live Pipeline Animation */}
      <PipelineTimeline status={video.status} />

      {/* Action Footer */}
      <div className="flex items-center justify-between p-4 glass-panel rounded-2xl border border-white/10">
        <div className="text-xs text-slate-400">
          {isCompleted
            ? 'All extracted modalities indexed inside ChromaDB vector store.'
            : 'Pipeline executing in background. Auto-polling server every 2 seconds.'}
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => navigate('/videos')}>
            View All Videos
          </Button>
          <Button
            size="sm"
            onClick={() => navigate(`/videos/${video.id}`)}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Open Video Details Inspector
          </Button>
        </div>
      </div>
    </div>
  );
};
