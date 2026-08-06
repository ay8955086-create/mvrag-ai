import React from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Bot, Search, BarChart3, Video, Sparkles } from 'lucide-react';
import { Card } from '../ui/Card';

export const QuickActions: React.FC = () => {
  const navigate = useNavigate();

  const actions = [
    {
      title: 'Upload New Video',
      desc: 'Drag & drop video for automatic AI pipeline extraction',
      icon: UploadCloud,
      path: '/upload',
      color: 'from-brand-600 to-indigo-600',
    },
    {
      title: 'Multimodal AI Chat',
      desc: 'Ask questions with auto vector retrieval & timestamp links',
      icon: Bot,
      path: '/chat',
      color: 'from-indigo-600 to-cyan-600',
    },
    {
      title: 'Semantic Video Search',
      desc: 'Search across speech, OCR text, and visual captions',
      icon: Search,
      path: '/search',
      color: 'from-purple-600 to-pink-600',
    },
    {
      title: 'View Video Library',
      desc: 'Inspect transcripts, OCR text, keyframes & embeddings',
      icon: Video,
      path: '/videos',
      color: 'from-blue-600 to-teal-600',
    },
  ];

  return (
    <Card glass className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-brand-400" />
          Quick Actions
        </h3>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {actions.map((action, idx) => {
          const Icon = action.icon;
          return (
            <div
              key={idx}
              onClick={() => navigate(action.path)}
              className="p-4 rounded-xl bg-slate-900/60 hover:bg-slate-900/90 border border-white/5 hover:border-brand-500/40 transition-all duration-300 cursor-pointer group flex flex-col justify-between"
            >
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${action.color} text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform mb-3`}>
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-200 group-hover:text-brand-300 transition-colors">{action.title}</h4>
                <p className="text-[10px] text-slate-400 mt-1 leading-snug">{action.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
