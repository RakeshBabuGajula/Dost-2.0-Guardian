import React from 'react';

export const TrackLegend: React.FC = () => {
  return (
    <div className="flex flex-wrap items-center gap-4 text-xs font-mono text-slate-300 bg-[#121826] p-3 rounded-xl border border-slate-800">
      <span className="text-slate-400 font-semibold uppercase text-[10px]">Map Legend:</span>
      
      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
        <span>Worker Safe</span>
      </div>

      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
        <span>Caution</span>
      </div>

      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded-full bg-orange-500 inline-block"></span>
        <span>Warning</span>
      </div>

      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded-full bg-red-500 animate-pulse inline-block"></span>
        <span>Critical / Unacknowledged</span>
      </div>

      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded bg-cyan-600 inline-block"></span>
        <span>Train Vector</span>
      </div>

      <div className="flex items-center space-x-1.5">
        <span className="w-3 h-3 rounded bg-emerald-950 border border-emerald-500 inline-block"></span>
        <span>Safe Refuge Niche</span>
      </div>
    </div>
  );
};
