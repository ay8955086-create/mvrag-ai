import React from 'react';
import { Sparkles, MessageSquare } from 'lucide-react';

interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

export const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({ onSelect }) => {
  const suggestions = [
    'Explain explicit typecasting from the video.',
    'What key concepts are discussed in the first half?',
    'Show OCR text detected on code snippets or slides.',
    'Summarize the main technical takeaways from this video.',
  ];

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
        <Sparkles className="w-3.5 h-3.5 text-brand-400" />
        <span>Suggested Prompts</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {suggestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(q)}
            className="p-3 text-left rounded-xl glass-panel hover:bg-slate-800/60 border border-white/5 hover:border-brand-500/30 text-xs text-slate-300 hover:text-white transition-all duration-200 flex items-start gap-2 group"
          >
            <MessageSquare className="w-3.5 h-3.5 text-slate-500 group-hover:text-brand-400 mt-0.5 flex-shrink-0" />
            <span className="line-clamp-2">{q}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
