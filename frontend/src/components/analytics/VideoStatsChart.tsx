import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { Card } from '../ui/Card';

export const VideoStatsChart: React.FC = () => {
  const data = [
    { day: 'Mon', videos: 4, chunks: 64, queries: 18 },
    { day: 'Tue', videos: 7, chunks: 112, queries: 32 },
    { day: 'Wed', videos: 5, chunks: 80, queries: 24 },
    { day: 'Thu', videos: 9, chunks: 144, queries: 45 },
    { day: 'Fri', videos: 12, chunks: 192, queries: 68 },
    { day: 'Sat', videos: 8, chunks: 128, queries: 39 },
    { day: 'Sun', videos: 14, chunks: 224, queries: 82 },
  ];

  return (
    <Card glass className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-100">Daily Ingestion & Query Volume</h3>
          <p className="text-[11px] text-slate-400">Total videos processed & RAG queries generated</p>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-semibold">
          <span className="flex items-center gap-1 text-brand-400">
            <span className="w-2 h-2 rounded-full bg-brand-500" />
            Chunks
          </span>
          <span className="flex items-center gap-1 text-cyan-400">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            Queries
          </span>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorChunks" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorQueries" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                fontSize: '12px',
              }}
            />
            <Area type="monotone" dataKey="chunks" stroke="#6366f1" fillOpacity={1} fill="url(#colorChunks)" strokeWidth={2} />
            <Area type="monotone" dataKey="queries" stroke="#06b6d4" fillOpacity={1} fill="url(#colorQueries)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};
