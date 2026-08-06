import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Video, Search, Filter, ArrowUpDown, UploadCloud, Trash2 } from 'lucide-react';
import { useVideos, useDeleteVideo } from '../hooks/useVideos';
import { VideoCard } from '../components/video/VideoCard';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Modal } from '../components/ui/Modal';
import { Skeleton } from '../components/ui/Skeleton';
import { Card } from '../components/ui/Card';

export const VideoLibrary: React.FC = () => {
  const navigate = useNavigate();
  const { data: videos, isLoading } = useVideos();
  const deleteMutation = useDeleteVideo();

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [sortBy, setSortBy] = useState<'newest' | 'title' | 'duration' | 'size'>('newest');
  const [deleteTargetId, setDeleteTargetId] = useState<number | null>(null);

  const filteredVideos = (videos || [])
    .filter((v) => {
      const matchesSearch =
        v.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        v.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (v.description && v.description.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesStatus = statusFilter === 'ALL' || v.status.toUpperCase() === statusFilter;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      if (sortBy === 'newest') return new Date(b.upload_time).getTime() - new Date(a.upload_time).getTime();
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'duration') return b.duration - a.duration;
      if (sortBy === 'size') return b.size_mb - a.size_mb;
      return 0;
    });

  const handleDeleteConfirm = () => {
    if (deleteTargetId !== null) {
      deleteMutation.mutate(deleteTargetId, {
        onSuccess: () => setDeleteTargetId(null),
      });
    }
  };

  return (
    <div className="space-y-6 pb-8">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
            <Video className="w-6 h-6 text-brand-400" />
            Video Repository Library
          </h1>
          <p className="text-xs text-slate-400">
            Browse, inspect, and manage all videos indexed with ChromaDB vector embeddings.
          </p>
        </div>

        <Button
          onClick={() => navigate('/upload')}
          leftIcon={<UploadCloud className="w-4 h-4" />}
          className="shadow-lg shadow-brand-500/20"
        >
          Upload Video
        </Button>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by title, filename, or context..."
            className="w-full pl-10 pr-4 py-2 bg-slate-900/80 border border-slate-700/80 rounded-xl text-xs text-slate-100 placeholder-slate-500 outline-none focus:border-brand-500"
          />
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          {/* Status Filter */}
          <div className="flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800 text-xs">
            {['ALL', 'COMPLETED', 'PROCESSING', 'FAILED'].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1.5 rounded-lg font-semibold text-[11px] transition-all ${
                  statusFilter === st ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {st}
              </button>
            ))}
          </div>

          {/* Sort By Dropdown */}
          <select
            value={sortBy}
            onChange={(e: any) => setSortBy(e.target.value)}
            className="bg-slate-900/80 border border-slate-700/80 text-slate-200 text-xs rounded-xl px-3 py-2 outline-none focus:border-brand-500"
          >
            <option value="newest">Sort: Newest First</option>
            <option value="title">Sort: Title (A-Z)</option>
            <option value="duration">Sort: Duration</option>
            <option value="size">Sort: File Size</option>
          </select>
        </div>
      </div>

      {/* Video Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <Skeleton className="h-72 w-full" />
          <Skeleton className="h-72 w-full" />
          <Skeleton className="h-72 w-full" />
        </div>
      ) : filteredVideos.length === 0 ? (
        <Card glass className="p-12 text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-slate-800 text-slate-400 mx-auto flex items-center justify-center">
            <Video className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-slate-200">No Videos Match Criteria</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Try adjusting your search query or status filter options.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredVideos.map((video) => (
            <VideoCard
              key={video.id}
              video={video}
              onDelete={(id) => setDeleteTargetId(id)}
            />
          ))}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={deleteTargetId !== null}
        onClose={() => setDeleteTargetId(null)}
        title="Delete Video Confirmation"
        description="Are you sure you want to delete this video? This action will permanently remove all audio, Whisper transcriptions, OCR text, and ChromaDB vector embeddings."
      >
        <div className="flex items-center justify-end gap-3 mt-6">
          <Button variant="ghost" onClick={() => setDeleteTargetId(null)}>
            Cancel
          </Button>
          <Button
            variant="danger"
            isLoading={deleteMutation.isPending}
            onClick={handleDeleteConfirm}
            leftIcon={<Trash2 className="w-4 h-4" />}
          >
            Delete Video
          </Button>
        </div>
      </Modal>
    </div>
  );
};
