import React, { ReactNode } from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: ReactNode;
  trend?: { value: string; positive: boolean };
  badgeColor?: 'default' | 'cyan' | 'emerald' | 'amber' | 'red';
  onClick?: () => void;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  badgeColor = 'default',
  onClick,
}) => {
  const borderColors = {
    default: 'border-slate-800 hover:border-slate-700',
    cyan: 'border-cyan-500/30 hover:border-cyan-500/50',
    emerald: 'border-emerald-500/30 hover:border-emerald-500/50',
    amber: 'border-amber-500/30 hover:border-amber-500/50',
    red: 'border-red-500/40 hover:border-red-500/60 shadow-lg shadow-red-950/20',
  };

  return (
    <div
      onClick={onClick}
      className={`bg-[#121826] border rounded-xl p-4 transition-all duration-200 ${borderColors[badgeColor]} ${
        onClick ? 'cursor-pointer hover:bg-[#1A2336]' : ''
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">{title}</span>
        {icon && <div className="p-2 rounded-lg bg-slate-800/60 text-slate-300">{icon}</div>}
      </div>

      <div className="mt-2 flex items-baseline justify-between">
        <span className="text-2xl font-bold font-mono text-slate-100">{value}</span>
        {trend && (
          <span
            className={`text-xs font-mono font-medium ${
              trend.positive ? 'text-emerald-400' : 'text-rose-400'
            }`}
          >
            {trend.positive ? '↑' : '↓'} {trend.value}
          </span>
        )}
      </div>

      {subtitle && <p className="mt-1 text-xs text-slate-400 truncate">{subtitle}</p>}
    </div>
  );
};
