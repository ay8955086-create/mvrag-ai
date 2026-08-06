import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Video,
  Mic,
  FileText,
  Image,
  Layers,
  BarChart3,
  Bot,
  ArrowLeft,
  Clock,
  HardDrive,
  Cpu,
  Database,
  Sparkles,
} from 'lucide-react';
import { useVideo } from '../hooks/useVideos';
import { videoService } from '../services/videoService';
import { VideoPlayer } from '../components/video/VideoPlayer';
import { TranscriptViewer } from '../components/video/TranscriptViewer';
import { OCRViewer } from '../components/video/OCRViewer';
import { FrameGallery } from '../components/video/FrameGallery';
import { Tabs } from '../components/ui/Tabs';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Skeleton } from '../components/ui/Skeleton';
import { formatDuration, formatFileSize, formatDate, getStatusBadgeClass } from '../utils/formatters';

export const VideoDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const videoId = Number(id);
  const navigate = useNavigate();

  const { data: rawVideo, isLoading, isError } = useVideo(videoId);
  const [activeTab, setActiveTab] = useState('transcript');
  const [seekTime, setSeekTime] = useState<number | null>(null);

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto space-y-6">
        <Skeleton className="h-96 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (isError || !rawVideo) {
    return (
      <Card glass className="max-w-xl mx-auto p-8 text-center space-y-4">
        <h2 className="text-lg font-bold text-rose-400">Video Not Found</h2>
        <p className="text-xs text-slate-400">Could not find details for Video ID #{id}.</p>
        <Button onClick={() => navigate('/videos')}>Back to Video Library</Button>
      </Card>
    );
  }

  const details = videoService.getExtendedDetails(rawVideo);

  const tabs = [
    { id: 'transcript', label: 'Whisper Transcript', icon: <Mic />, count: details.transcripts?.length },
    { id: 'ocr', label: 'OCR Frame Text', icon: <FileText />, count: details.ocr_results?.length },
    { id: 'captions', label: 'BLIP Vision Captions', icon: <Image />, count: details.captions?.length },
    { id: 'chunks', label: 'ChromaDB Chunks', icon: <Layers />, count: details.chunks?.length },
    { id: 'stats', label: 'Processing Statistics', icon: <BarChart3 /> },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-8">
      {/* Top Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate('/videos')}
            className="text-slate-400 hover:text-white"
          >
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full border ${getStatusBadgeClass(details.status)} uppercase`}>
                {details.status}
              </span>
              <span className="text-xs font-mono text-slate-400">ID: #{details.id}</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">{details.title}</h1>
          </div>
        </div>

        <Button
          onClick={() => navigate(`/chat?videoId=${details.id}`)}
          leftIcon={<Bot className="w-4 h-4 text-white" />}
          className="shadow-xl shadow-brand-500/25"
        >
          Ask AI About This Video
        </Button>
      </div>

      {/* Main Grid: Player + Inspector Tabs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Video Player & Metadata Card */}
        <div className="lg:col-span-5 space-y-4">
          <VideoPlayer
            filename={details.filename}
            title={details.title}
            seekTimestamp={seekTime}
          />

          {/* Metadata Card */}
          <Card glass className="p-5 space-y-3">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Video Specifications</h3>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Duration</span>
                <span className="font-mono font-bold text-slate-200">{formatDuration(details.duration)}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px]">File Size</span>
                <span className="font-mono font-bold text-slate-200">{formatFileSize(details.size_mb)}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Resolution</span>
                <span className="font-mono font-bold text-slate-200">{details.width}x{details.height}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Frame Rate</span>
                <span className="font-mono font-bold text-slate-200">{details.fps} FPS</span>
              </div>
            </div>

            <div className="pt-2 border-t border-white/5 text-[11px] text-slate-400 space-y-1">
              <div><span className="text-slate-500">Uploaded:</span> {formatDate(details.upload_time)}</div>
              <div><span className="text-slate-500">Filename:</span> <span className="font-mono text-brand-300">{details.filename}</span></div>
            </div>
          </Card>
        </div>

        {/* Right Column: Multimodal Extraction Tabs */}
        <div className="lg:col-span-7 space-y-4">
          <Tabs
            tabs={tabs}
            activeTab={activeTab}
            onChange={(t) => setActiveTab(t)}
          />

          <Card glass className="p-6 min-h-[480px]">
            {activeTab === 'transcript' && (
              <TranscriptViewer
                segments={details.transcripts}
                onTimestampClick={(t) => setSeekTime(t)}
              />
            )}

            {activeTab === 'ocr' && (
              <OCRViewer
                ocrResults={details.ocr_results}
                onTimestampClick={(t) => setSeekTime(t)}
              />
            )}

            {activeTab === 'captions' && (
              <FrameGallery
                captions={details.captions}
                onTimestampClick={(t) => setSeekTime(t)}
              />
            )}

            {activeTab === 'chunks' && (
              <div className="space-y-3 max-h-[450px] overflow-y-auto pr-1">
                {details.chunks?.map((chunk) => (
                  <div key={chunk.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="font-mono font-bold text-brand-300">Chunk #{chunk.chunk_index}</span>
                      <span className="font-mono text-slate-400">
                        {formatDuration(chunk.start_time)} - {formatDuration(chunk.end_time)}
                      </span>
                    </div>
                    <p className="text-xs text-slate-200 leading-relaxed font-sans">{chunk.combined_text}</p>
                    <div className="flex items-center gap-1.5 text-[10px] text-slate-500 font-mono pt-1">
                      <Database className="w-3 h-3 text-cyan-400" />
                      <span>Vector Embedding ID: {chunk.embedding_id}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'stats' && details.processing_stats && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                  <span className="text-xs font-semibold text-slate-400">Total Processing Time</span>
                  <p className="text-2xl font-extrabold text-brand-300 font-mono">{details.processing_stats.processing_time}s</p>
                </div>
                <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                  <span className="text-xs font-semibold text-slate-400">Speech Segments Extracted</span>
                  <p className="text-2xl font-extrabold text-indigo-300 font-mono">{details.processing_stats.transcript_segments}</p>
                </div>
                <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                  <span className="text-xs font-semibold text-slate-400">OCR Detections</span>
                  <p className="text-2xl font-extrabold text-cyan-300 font-mono">{details.processing_stats.ocr_detections}</p>
                </div>
                <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                  <span className="text-xs font-semibold text-slate-400">Vision Captions Generated</span>
                  <p className="text-2xl font-extrabold text-emerald-300 font-mono">{details.processing_stats.caption_count}</p>
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
