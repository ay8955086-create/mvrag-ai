import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, FileVideo, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';
import { useUploadVideo } from '../hooks/useVideos';
import { DropZone } from '../components/upload/DropZone';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import { toast } from 'sonner';

export const UploadVideo: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [progress, setProgress] = useState(0);

  const uploadMutation = useUploadVideo();

  const handleUploadSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      toast.error('Please select a video file to upload.');
      return;
    }
    if (!title.trim()) {
      toast.error('Please enter a title for the video.');
      return;
    }

    uploadMutation.mutate(
      {
        file,
        title: title.trim(),
        description: description.trim() || undefined,
        onProgress: (p) => setProgress(p),
      },
      {
        onSuccess: (data) => {
          navigate(`/processing/${data.id}`);
        },
      }
    );
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
          <UploadCloud className="w-6 h-6 text-brand-400" />
          Upload & Index Video
        </h1>
        <p className="text-xs text-slate-400">
          Upload raw video files to initiate the automated audio, speech, OCR, vision & ChromaDB embedding pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Form & Uploader */}
        <div className="md:col-span-2 space-y-6">
          <form onSubmit={handleUploadSubmit} className="space-y-6">
            <Card glass className="p-6 space-y-4">
              <h3 className="text-sm font-bold text-slate-200">1. Video Details</h3>
              <Input
                label="Video Title *"
                placeholder="e.g. Explicit Typecasting and Memory Layout in C++"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />

              <div className="space-y-1.5">
                <label className="block text-xs font-medium text-slate-300">
                  Description (Optional)
                </label>
                <textarea
                  rows={3}
                  placeholder="Add context or notes about this video..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full rounded-xl bg-slate-900/60 border border-slate-700/60 text-slate-100 placeholder-slate-500 text-xs p-3 outline-none focus:border-brand-500 transition-all"
                />
              </div>
            </Card>

            <Card glass className="p-6 space-y-4">
              <h3 className="text-sm font-bold text-slate-200">2. Select Video File</h3>
              <DropZone
                onFileSelect={(selected) => {
                  setFile(selected);
                  if (!title) {
                    // Auto-fill title from filename
                    const baseName = selected.name.replace(/\.[^/.]+$/, '');
                    setTitle(baseName.replace(/[-_]/g, ' '));
                  }
                }}
                uploadProgress={progress}
                isUploading={uploadMutation.isPending}
              />
            </Card>

            <Button
              type="submit"
              size="lg"
              isLoading={uploadMutation.isPending}
              disabled={!file || !title.trim() || uploadMutation.isPending}
              className="w-full shadow-xl shadow-brand-500/25"
              rightIcon={<ArrowRight className="w-5 h-5" />}
            >
              Start Automated AI Pipeline Processing
            </Button>
          </form>
        </div>

        {/* Right Column: Pipeline Guide */}
        <div className="space-y-4">
          <Card glass className="p-6 space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-400" />
              Automated Pipeline Stages
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Once uploaded, our backend automatically executes the following 10 processing stages:
            </p>

            <ol className="space-y-2.5 text-xs text-slate-300 font-mono">
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">1</span>
                <span>Audio Track Extraction</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">2</span>
                <span>Whisper AI Speech Transcription</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">3</span>
                <span>OCR Text Detection on Frames</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">4</span>
                <span>BLIP Vision Caption Generation</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">5</span>
                <span>Multimodal Semantic Chunking</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-500/20 text-brand-300 flex items-center justify-center text-[10px] font-bold">6</span>
                <span>ChromaDB Vector Store Ingestion</span>
              </li>
            </ol>
          </Card>
        </div>
      </div>
    </div>
  );
};
