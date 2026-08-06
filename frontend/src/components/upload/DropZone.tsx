import React, { useState, useRef } from 'react';
import { UploadCloud, FileVideo, X, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '../ui/Button';
import { Progress } from '../ui/Progress';
import { formatFileSize } from '../../utils/formatters';

interface DropZoneProps {
  onFileSelect: (file: File) => void;
  uploadProgress?: number;
  isUploading?: boolean;
  onCancel?: () => void;
}

export const DropZone: React.FC<DropZoneProps> = ({
  onFileSelect,
  uploadProgress = 0,
  isUploading = false,
  onCancel,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const ALLOWED_TYPES = ['.mp4', '.avi', '.mov', '.mkv'];

  const validateAndSetFile = (file: File) => {
    setError(null);
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ALLOWED_TYPES.includes(ext)) {
      setError(`Unsupported video format. Allowed formats: ${ALLOWED_TYPES.join(', ')}`);
      return;
    }
    setSelectedFile(file);
    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative p-8 md:p-12 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-300 text-center flex flex-col items-center justify-center ${
          isDragOver
            ? 'border-brand-500 bg-brand-500/10 scale-[1.01]'
            : 'border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/80'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/mp4,video/avi,video/quicktime,video/x-matroska"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              validateAndSetFile(e.target.files[0]);
            }
          }}
        />

        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600/30 to-indigo-500/20 text-brand-400 border border-brand-500/30 flex items-center justify-center mb-4 shadow-xl">
          <UploadCloud className="w-8 h-8" />
        </div>

        <h3 className="text-base font-bold text-slate-100">
          Drag & Drop Video Here
        </h3>
        <p className="text-xs text-slate-400 mt-1 max-w-sm">
          Supports MP4, AVI, MOV, MKV files up to 2GB for automatic audio, transcript, OCR, and ChromaDB vector extraction.
        </p>

        <div className="mt-4 flex items-center gap-2 text-[11px] text-slate-500">
          <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono">MP4</span>
          <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono">AVI</span>
          <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono">MOV</span>
          <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono">MKV</span>
        </div>
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {selectedFile && (
        <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileVideo className="w-6 h-6 text-brand-400" />
              <div>
                <h4 className="text-xs font-bold text-slate-200 truncate max-w-xs">{selectedFile.name}</h4>
                <p className="text-[10px] text-slate-400">{formatFileSize(selectedFile.size / (1024 * 1024))}</p>
              </div>
            </div>
            {isUploading && onCancel && (
              <Button variant="ghost" size="sm" onClick={onCancel} className="text-rose-400">
                <X className="w-3.5 h-3.5" />
                <span>Cancel</span>
              </Button>
            )}
          </div>

          {isUploading && (
            <div className="space-y-1.5">
              <div className="flex justify-between text-[10px] font-mono text-slate-400">
                <span>Uploading to Backend...</span>
                <span>{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} animated />
            </div>
          )}
        </div>
      )}
    </div>
  );
};
