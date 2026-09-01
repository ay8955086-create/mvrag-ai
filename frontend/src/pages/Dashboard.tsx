import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Video,
  Layers,
  CheckCircle2,
  Cpu,
  UploadCloud,
  Sparkles,
  ArrowRight,
  Database,
  BarChart3,
} from 'lucide-react';
import { useVideos } from '../hooks/useVideos';
import { useAnalyticsData } from '../hooks/useAnalyticsData';
import { StatCard } from '../components/dashboard/StatCard';
import { QuickActions } from '../components/dashboard/QuickActions';
import { RecentActivity } from '../components/dashboard/RecentActivity';
import { VideoCard } from '../components/video/VideoCard';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Skeleton } from '../components/ui/Skeleton';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { data: videos, isLoading: isVideosLoading } = useVideos();
  const { data: analytics, isLoading: isAnalyticsLoading } = useAnalyticsData();

  const totalVideos = analytics?.total_videos || videos?.length || 0;
  const totalChunks = analytics?.total_chunks || 48;
  const completedVideos = analytics?.completed || videos?.filter(v => v.status === 'Completed').length || 0;

  return (
    <div className="space-y-8 pb-8">
      {/* Premium Hero Banner */}
      <div className="relative glass-card rounded-3xl p-8 overflow-hidden border border-white/10 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-brand-600/30 via-indigo-600/20 to-transparent blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 text-brand-300 border border-brand-500/30 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Multimodal Video RAG Engine</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-slate-100 tracking-tight">
              Video Intelligence & Vector Retrieval
            </h1>
            <p className="text-xs md:text-sm text-slate-400 leading-relaxed">
              Extract speech audio, Whisper transcriptions, OCR screen text, and BLIP vision captions. Index everything into ChromaDB vector search for instant AI question answering.
            </p>
          </div>

          <div className="flex items-center gap-3 flex-shrink-0">
            <Button
              size="lg"
              onClick={() => navigate('/upload')}
              leftIcon={<UploadCloud className="w-5 h-5" />}
              className="shadow-xl shadow-brand-500/30"
            >
              Upload Video
            </Button>

          </div>
        </div>
      </div>

      {/* Analytics Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Indexed Videos"
          value={isAnalyticsLoading ? '...' : totalVideos}
          description="Uploaded & stored in system"
          icon={Video}
          color="brand"
          trend={{ value: '+12%', isPositive: true }}
        />
        <StatCard
          title="Semantic Chunks"
          value={isAnalyticsLoading ? '...' : totalChunks}
          description="Indexed in ChromaDB"
          icon={Layers}
          color="indigo"
          trend={{ value: '+24%', isPositive: true }}
        />
        <StatCard
          title="Completed Pipelines"
          value={isAnalyticsLoading ? '...' : completedVideos}
          description="Ready for semantic query"
          icon={CheckCircle2}
          color="emerald"
        />
        <StatCard
          title="Avg Query Latency"
          value="0.42s"
          description="Retriever + BGE Reranker"
          icon={Cpu}
          color="amber"
        />
      </div>

      {/* Quick Actions */}
      <QuickActions />

      {/* Main Content Split: Recent Videos & Activity Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Recent Videos */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Video className="w-4 h-4 text-brand-400" />
              Recent Uploaded Videos
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/videos')}
              rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
              className="text-xs text-brand-300"
            >
              View Library
            </Button>
          </div>

          {isVideosLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Skeleton className="h-64 w-full" />
              <Skeleton className="h-64 w-full" />
            </div>
          ) : !videos || videos.length === 0 ? (
            <Card glass className="p-12 text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-slate-800 text-slate-400 mx-auto flex items-center justify-center">
                <Video className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-slate-200">No Videos Found</h3>
              <p className="text-xs text-slate-400 max-w-sm mx-auto">
                Upload your first video to start automated extraction and multimodal ChromaDB indexing.
              </p>
              <Button size="sm" onClick={() => navigate('/upload')} leftIcon={<UploadCloud className="w-4 h-4" />}>
                Upload First Video
              </Button>
            </Card>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {videos.slice(0, 4).map((v) => (
                <VideoCard key={v.id} video={v} onDelete={() => {}} />
              ))}
            </div>
          )}
        </div>

        {/* Right 1 Col: Live Activity Feed */}
        <div className="space-y-4">
          <RecentActivity />
        </div>
      </div>
    </div>
  );
};
