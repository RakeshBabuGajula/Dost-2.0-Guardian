import React from 'react';
import { Settings, Sliders, Shield, Info } from 'lucide-react';

export const SettingsView: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-slate-800 text-slate-300">
            <Settings className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">SAFETY RULE PARAMETER CONFIGURATION</h2>
            <p className="text-xs text-slate-400">Configurable thresholds & perception reaction time buffers</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-amber-500/20 text-amber-300 rounded-lg text-xs font-mono font-bold">
          SIMULATION VALUE / REQUIRES RAILWAY AUTHORIZATION
        </span>
      </div>

      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-5 space-y-4">
        <div className="space-y-3 font-mono text-xs">
          <div className="flex justify-between items-center py-2 border-b border-slate-800">
            <span className="text-slate-300">Critical Alert Time-to-Danger (TTD) Threshold</span>
            <input type="number" defaultValue={90} className="w-20 bg-slate-900 border border-slate-700 text-cyan-300 px-2 py-1 rounded" />
          </div>
          <div className="flex justify-between items-center py-2 border-b border-slate-800">
            <span className="text-slate-300">Warning State TTD Threshold</span>
            <input type="number" defaultValue={180} className="w-20 bg-slate-900 border border-slate-700 text-cyan-300 px-2 py-1 rounded" />
          </div>
          <div className="flex justify-between items-center py-2 border-b border-slate-800">
            <span className="text-slate-300">Caution State TTD Threshold</span>
            <input type="number" defaultValue={300} className="w-20 bg-slate-900 border border-slate-700 text-cyan-300 px-2 py-1 rounded" />
          </div>
          <div className="flex justify-between items-center py-2 border-b border-slate-800">
            <span className="text-slate-300">Supervisor Tier-1 Escalation Timer (T1)</span>
            <input type="number" defaultValue={10} className="w-20 bg-slate-900 border border-slate-700 text-cyan-300 px-2 py-1 rounded" />
          </div>
          <div className="flex justify-between items-center py-2">
            <span className="text-slate-300">Control Room Tier-2 Escalation Timer (T2)</span>
            <input type="number" defaultValue={20} className="w-20 bg-slate-900 border border-slate-700 text-cyan-300 px-2 py-1 rounded" />
          </div>
        </div>
      </div>
    </div>
  );
};
