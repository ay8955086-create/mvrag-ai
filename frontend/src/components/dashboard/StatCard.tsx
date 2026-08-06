import React from 'react';
import { Card } from '../ui/Card';

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: any;
  trend?: {
    value: string;
    isPositive: boolean;
  };
  color?: 'brand' | 'emerald' | 'amber' | 'indigo';
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  description,
  icon: Icon,
  trend,
  color = 'brand',
}) => {
  const colorMap = {
    brand: 'from-brand-600/20 to-indigo-500/10 text-brand-400 border-brand-500/30',
    emerald: 'from-emerald-600/20 to-teal-500/10 text-emerald-400 border-emerald-500/30',
    amber: 'from-amber-600/20 to-yellow-500/10 text-amber-400 border-amber-500/30',
    indigo: 'from-indigo-600/20 to-purple-500/10 text-indigo-400 border-indigo-500/30',
  };

  return (
    <Card hoverGlow className="p-5 flex flex-col justify-between">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
          <h3 className="text-2xl font-extrabold text-slate-100 mt-1 font-mono tracking-tight">{value}</h3>
        </div>

        <div className={`p-3 rounded-2xl bg-gradient-to-tr border shadow-lg ${colorMap[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      {(description || trend) && (
        <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs">
          {description && <span className="text-slate-400">{description}</span>}
          {trend && (
            <span
              className={`font-semibold font-mono px-2 py-0.5 rounded-full text-[10px] ${
                trend.isPositive ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
              }`}
            >
              {trend.isPositive ? '+' : ''}
              {trend.value}
            </span>
          )}
        </div>
      )}
    </Card>
  );
};
