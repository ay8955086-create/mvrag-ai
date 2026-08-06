import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { Card } from '../ui/Card';

export const StorageChart: React.FC = () => {
  const data = [
    { name: 'Raw Videos', value: 450, color: '#6366f1' },
    { name: 'ChromaDB Embeddings', value: 180, color: '#06b6d4' },
    { name: 'Extracted Frames & OCR', value: 120, color: '#10b981' },
    { name: 'Audio Tracks', value: 90, color: '#f59e0b' },
  ];

  return (
    <Card glass className="p-6">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-bold text-slate-100">Storage Allocation</h3>
        <span className="text-xs font-mono font-semibold text-brand-300">840 MB Total</span>
      </div>
      <p className="text-[11px] text-slate-400 mb-4">Breakdown of local data & vector index storage</p>

      <div className="h-56 w-full flex items-center justify-center">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                fontSize: '12px',
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-white/5">
        {data.map((item, idx) => (
          <div key={idx} className="flex items-center gap-2 text-[11px]">
            <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
            <span className="text-slate-400 truncate">{item.name}</span>
            <span className="text-slate-200 font-mono ml-auto">{item.value} MB</span>
          </div>
        ))}
      </div>
    </Card>
  );
};
