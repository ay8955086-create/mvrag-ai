import React, { useEffect, useState } from 'react';
import {
  UploadCloud,
  Volume2,
  Mic,
  FileText,
  Image,
  Sparkles,
  Layers,
  Cpu,
  Database,
  CheckCircle2,
  Loader2,
  AlertCircle,
} from 'lucide-react';
import { Progress } from '../ui/Progress';
import { Card } from '../ui/Card';

interface PipelineStepItem {
  id: string;
  label: string;
  desc: string;
  icon: any;
}

interface PipelineTimelineProps {
  status: 'Pending' | 'Processing' | 'Completed' | 'Failed';
  currentStepIndex?: number;
}

export const PipelineTimeline: React.FC<PipelineTimelineProps> = ({
  status,
  currentStepIndex: initialStepIndex = 0,
}) => {
  const steps: PipelineStepItem[] = [
    { id: 'upload', label: 'Uploading', desc: 'Receiving raw video stream', icon: UploadCloud },
    { id: 'audio', label: 'Extracting Audio', desc: 'Separating 16kHz WAV track', icon: Volume2 },
    { id: 'whisper', label: 'Speech to Text', desc: 'Whisper AI transcription', icon: Mic },
    { id: 'ocr', label: 'OCR Extraction', desc: 'Scanning keyframes for text', icon: FileText },
    { id: 'frames', label: 'Frame Extraction', desc: 'Sampling video keyframes', icon: Image },
    { id: 'blip', label: 'BLIP Captioning', desc: 'Generating vision captions', icon: Sparkles },
    { id: 'chunking', label: 'Semantic Chunking', desc: 'Aligning multimodal segments', icon: Layers },
    { id: 'embedding', label: 'Vector Embedding', desc: 'Generating dense embeddings', icon: Cpu },
    { id: 'chromadb', label: 'ChromaDB Indexing', desc: 'Storing in vector database', icon: Database },
    { id: 'completed', label: 'Completed', desc: 'Pipeline ready for AI queries', icon: CheckCircle2 },
  ];

  const [activeStep, setActiveStep] = useState(initialStepIndex);

  useEffect(() => {
    if (status === 'Completed') {
      setActiveStep(steps.length - 1);
      return;
    }
    if (status === 'Processing') {
      const interval = setInterval(() => {
        setActiveStep((prev) => (prev < steps.length - 2 ? prev + 1 : prev));
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [status, steps.length]);

  const progressPercent = Math.round(((activeStep + 1) / steps.length) * 100);

  return (
    <Card glass className="p-6 space-y-6">
      {/* Header Info */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            Multimodal Video Processing Pipeline
            {status === 'Processing' && (
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse">
                Active Execution
              </span>
            )}
            {status === 'Completed' && (
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                100% Indexed
              </span>
            )}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time stage timeline of audio, speech, OCR, vision & ChromaDB vector ingestion.
          </p>
        </div>
        <span className="text-xs font-mono font-bold text-brand-300 bg-brand-500/10 px-3 py-1 rounded-xl border border-brand-500/30">
          {progressPercent}% Completed
        </span>
      </div>

      <Progress value={progressPercent} animated={status === 'Processing'} size="md" />

      {/* Steps Timeline Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          const isDone = idx < activeStep || status === 'Completed';
          const isCurrent = idx === activeStep && status === 'Processing';
          const isPending = idx > activeStep && status !== 'Completed';

          return (
            <div
              key={step.id}
              className={`p-3.5 rounded-xl border transition-all duration-300 flex flex-col justify-between ${
                isDone
                  ? 'bg-emerald-500/5 border-emerald-500/20 text-slate-200'
                  : isCurrent
                  ? 'bg-brand-500/15 border-brand-500/50 shadow-lg shadow-brand-500/10 text-white scale-[1.02]'
                  : 'bg-slate-900/40 border-slate-800/80 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center ${
                    isDone
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : isCurrent
                      ? 'bg-brand-600 text-white shadow-md'
                      : 'bg-slate-800 text-slate-500'
                  }`}
                >
                  {isCurrent ? <Loader2 className="w-4 h-4 animate-spin" /> : <Icon className="w-4 h-4" />}
                </div>
                <span className="text-[10px] font-mono font-bold text-slate-500">0{idx + 1}</span>
              </div>

              <div>
                <h4 className={`text-xs font-bold ${isCurrent ? 'text-brand-300' : isDone ? 'text-slate-200' : 'text-slate-400'}`}>
                  {step.label}
                </h4>
                <p className="text-[10px] text-slate-500 mt-0.5 line-clamp-1">{step.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
