import React from 'react';
import { Activity, CheckCircle2, Clock, Bot, Search, Film } from 'lucide-react';
import { Card } from '../ui/Card';

export const RecentActivity: React.FC = () => {
  const activities = [
    {
      id: '1',
      title: 'Video Indexing Completed',
      desc: 'ChromaDB stored 48 semantic chunks for "Explicit Typecasting Demo.mp4"',
      time: '10 mins ago',
      icon: CheckCircle2,
      color: 'text-emerald-400',
    },
    {
      id: '2',
      title: 'Multimodal RAG Query',
      desc: 'User asked: "Explain explicit typecasting from the video"',
      time: '25 mins ago',
      icon: Bot,
      color: 'text-brand-400',
    },
    {
      id: '3',
      title: 'Whisper Speech Transcription',
      desc: 'Extracted 34 timestamps with 98.4% language accuracy',
      time: '1 hour ago',
      icon: Film,
      color: 'text-indigo-400',
    },
  ];

  return (
    <Card glass className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <Activity className="w-4 h-4 text-brand-400" />
          Recent Activity Feed
        </h3>
        <span className="text-[10px] text-slate-400 font-mono">Live Logs</span>
      </div>

      <div className="space-y-3">
        {activities.map((act) => {
          const Icon = act.icon;
          return (
            <div key={act.id} className="p-3 rounded-xl bg-slate-900/40 border border-white/5 flex items-start gap-3 text-xs">
              <div className={`p-2 rounded-lg bg-slate-800/80 ${act.color} mt-0.5`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-slate-200">{act.title}</h4>
                  <span className="text-[10px] text-slate-500 font-mono">{act.time}</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-0.5">{act.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
