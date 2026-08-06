import React from 'react';
import { Sparkles, Layers, Cpu, Database, Film, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { Card } from '../components/ui/Card';

export const About: React.FC = () => {
  const features = [
    { title: 'Audio Extraction', desc: 'Converts raw video into 16kHz mono WAV tracks' },
    { title: 'Whisper Transcription', desc: 'Extracts time-aligned speech segments with word confidence' },
    { title: 'OCR Frame Scanning', desc: 'Extracts text, slide headers, and code snippets from keyframes' },
    { title: 'BLIP Vision Captions', desc: 'Generates high-level visual descriptions using vision transformers' },
    { title: 'ChromaDB Vector Store', desc: 'Indexes multimodal embeddings for hybrid semantic search' },
    { title: 'Cross-Encoder Reranker', desc: 'Re-scores candidate chunks using BGE-Reranker for precision' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="glass-card rounded-3xl p-8 border border-white/10 space-y-3 text-center">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-cyan-400 text-white mx-auto flex items-center justify-center shadow-lg">
          <Sparkles className="w-6 h-6 animate-pulse" />
        </div>
        <h1 className="text-3xl font-extrabold text-slate-100 tracking-tight">MVRAG AI Architecture</h1>
        <p className="text-xs text-slate-400 max-w-xl mx-auto">
          State of the Art Multimodal Video Retrieval-Augmented Generation Platform.
        </p>
      </div>

      {/* Feature Architecture Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((f, i) => (
          <Card key={i} glass className="p-5 space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
              <CheckCircle2 className="w-4 h-4 text-brand-400" />
              {f.title}
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">{f.desc}</p>
          </Card>
        ))}
      </div>

      {/* Technology Stack Details */}
      <Card glass className="p-6 space-y-4">
        <h3 className="text-sm font-bold text-slate-100">Technology Stack & Specifications</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px]">Backend</span>
            <span className="text-brand-300 font-bold">FastAPI</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px]">Vector DB</span>
            <span className="text-indigo-300 font-bold">ChromaDB</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px]">Speech AI</span>
            <span className="text-cyan-300 font-bold">Whisper</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px]">Frontend</span>
            <span className="text-emerald-300 font-bold">React 19 + Vite</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
