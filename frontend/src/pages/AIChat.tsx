import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Bot, Sparkles, Video } from 'lucide-react';
import { useVideos } from '../hooks/useVideos';
import { ChatContainer } from '../components/chat/ChatContainer';
import { VideoPlayer } from '../components/video/VideoPlayer';
import { Card } from '../components/ui/Card';

export const AIChat: React.FC = () => {
  const [searchParams] = useSearchParams();
  const videoIdParam = searchParams.get('videoId');
  const initialVideoId = videoIdParam ? Number(videoIdParam) : null;

  const [selectedVideoId, setSelectedVideoId] = useState<number | null>(initialVideoId);
  const [seekTime, setSeekTime] = useState<number | null>(null);

  const { data: videos } = useVideos();
  const selectedVideo = videos?.find((v) => v.id === selectedVideoId);

  useEffect(() => {
    if (videoIdParam) {
      setSelectedVideoId(Number(videoIdParam));
    }
  }, [videoIdParam]);

  return (
    <div className="space-y-4 pb-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
            <Bot className="w-6 h-6 text-brand-400" />
            AI RAG Chat Assistant
          </h1>
          <p className="text-xs text-slate-400">
            Ask questions over ChromaDB vector embeddings across speech, OCR text, and visual frame captions.
          </p>
        </div>
      </div>

      <div className={`grid grid-cols-1 ${selectedVideo ? 'lg:grid-cols-12' : ''} gap-6`}>
        {/* Chat Container */}
        <div className={selectedVideo ? 'lg:col-span-7' : 'w-full'}>
          <ChatContainer
            videos={videos}
            selectedVideoId={selectedVideoId}
            onSelectVideo={(id) => setSelectedVideoId(id)}
            onOpenTimestamp={(t) => setSeekTime(t)}
          />
        </div>

        {/* Optional Side Video Player when scoped */}
        {selectedVideo && (
          <div className="lg:col-span-5 space-y-4">
            <Card glass className="p-4 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-200 flex items-center gap-1.5">
                  <Video className="w-3.5 h-3.5 text-brand-400" />
                  Active Video Preview
                </span>
                <span className="text-[10px] text-slate-400 font-mono">ID: #{selectedVideo.id}</span>
              </div>

              <VideoPlayer
                filename={selectedVideo.filename}
                title={selectedVideo.title}
                seekTimestamp={seekTime}
              />

              <div className="text-[11px] text-slate-400 p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                Click timestamp citation buttons in chat responses to jump the video directly to that segment!
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};
