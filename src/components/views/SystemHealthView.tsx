import React from 'react';
import { SimulationState } from '../../types/simulation';
import { Activity, Server, Database, Radio, Cpu, HardDrive } from 'lucide-react';

interface SystemHealthViewProps {
  state: SimulationState;
}

export const SystemHealthView: React.FC<SystemHealthViewProps> = ({ state }) => {
  return (
    <div className="space-y-6">
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">SYSTEM & HARDWARE HEALTH DASHBOARD</h2>
            <p className="text-xs text-slate-400">Infrastructure latency, WebSocket connection & endpoint health</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg text-xs font-mono font-bold">
          ALL SYSTEMS HEALTHY
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {state.systemHealth.map((item) => (
          <div key={item.component} className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-slate-200">{item.component}</span>
              <span className="px-2 py-0.5 text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 rounded">
                {item.status}
              </span>
            </div>
            <div className="text-xl font-bold font-mono text-cyan-400">{item.latencyMs} ms latency</div>
            <div className="text-[11px] font-mono text-slate-400">Last Ping: {item.lastSyncTimestamp}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
