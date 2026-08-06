import React from 'react';
import { clsx } from 'clsx';

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number; // 0 to 100
  size?: 'sm' | 'md' | 'lg';
  animated?: boolean;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  size = 'md',
  animated = false,
  className,
  ...props
}) => {
  const clampedValue = Math.min(100, Math.max(0, value));

  const heights = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  };

  return (
    <div
      className={clsx('w-full bg-slate-800/80 rounded-full overflow-hidden border border-slate-700/40', heights[size], className)}
      {...props}
    >
      <div
        className={clsx(
          'h-full bg-gradient-to-r from-brand-600 via-indigo-500 to-cyan-400 rounded-full transition-all duration-300 ease-out',
          animated && 'relative after:absolute after:inset-0 after:bg-white/20 after:animate-shimmer'
        )}
        style={{ width: `${clampedValue}%` }}
      />
    </div>
  );
};
