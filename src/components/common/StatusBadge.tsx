import React from 'react';
import { SafetyState } from '../../types/safety';

interface StatusBadgeProps {
  status: SafetyState | string;
  size?: 'sm' | 'md' | 'lg';
  showDot?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md', showDot = true }) => {
  let bgClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
  let dotClass = 'bg-emerald-500 animate-pulse';
  let label = status;

  switch (status) {
    case 'SAFE':
      bgClass = 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
      dotClass = 'bg-emerald-500';
      label = 'SAFE';
      break;
    case 'CAUTION':
      bgClass = 'bg-amber-500/15 text-amber-400 border-amber-500/30';
      dotClass = 'bg-amber-500';
      label = 'CAUTION';
      break;
    case 'WARNING':
      bgClass = 'bg-orange-500/20 text-orange-400 border-orange-500/40';
      dotClass = 'bg-orange-500 animate-ping';
      label = 'WARNING';
      break;
    case 'CRITICAL':
      bgClass = 'bg-red-500/25 text-red-400 border-red-500/50 shadow-lg shadow-red-500/20';
      dotClass = 'bg-red-500 animate-ping';
      label = 'CRITICAL';
      break;
    case 'EMERGENCY':
      bgClass = 'bg-rose-600/30 text-rose-300 border-rose-500/60 shadow-lg shadow-rose-600/30 animate-pulse';
      dotClass = 'bg-rose-500 animate-bounce';
      label = 'EMERGENCY';
      break;
    case 'DEGRADED_NETWORK':
      bgClass = 'bg-orange-600/20 text-orange-300 border-orange-500/40';
      dotClass = 'bg-orange-400';
      label = 'DEGRADED NETWORK';
      break;
    case 'OFFLINE':
      bgClass = 'bg-slate-700/30 text-slate-400 border-slate-600/30';
      dotClass = 'bg-slate-500';
      label = 'OFFLINE';
      break;
  }

  const sizeClasses = {
    sm: 'text-[10px] px-2 py-0.5 space-x-1',
    md: 'text-xs px-2.5 py-1 space-x-1.5',
    lg: 'text-sm px-3.5 py-1.5 space-x-2 font-semibold',
  };

  return (
    <span className={`inline-flex items-center rounded-full border font-mono tracking-wide ${sizeClasses[size]} ${bgClass}`}>
      {showDot && <span className={`inline-block rounded-full ${size === 'sm' ? 'w-1.5 h-1.5' : 'w-2 h-2'} ${dotClass}`} />}
      <span>{label}</span>
    </span>
  );
};
