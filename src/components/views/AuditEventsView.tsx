import React from 'react';
import { SimulationState } from '../../types/simulation';
import { FileCheck2, ShieldCheck, Terminal } from 'lucide-react';

interface AuditEventsViewProps {
  state: SimulationState;
}

export const AuditEventsView: React.FC<AuditEventsViewProps> = ({ state }) => {
  return (
    <div className="space-y-6">
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
            <FileCheck2 className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">IMMUTABLE SAFETY AUDIT LOG STREAM</h2>
            <p className="text-xs text-slate-400">7-Year retention audit compliance event record stream</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-slate-900 border border-slate-800 text-cyan-400 rounded-lg text-xs font-mono">
          APPEND-ONLY VAULT
        </span>
      </div>

      <div className="bg-[#090D16] border border-slate-800 rounded-2xl p-4 font-mono text-xs text-slate-300 space-y-2 max-h-[500px] overflow-y-auto shadow-inner">
        <div className="text-slate-500 text-[11px] mb-2">// Showing real-time event stream (Tick #{state.tickCount})</div>
        <div className="text-cyan-400">[{state.simulationTime}] EVENT_INGRESS: TRAIN_POSITION_UPDATE (EXP-12626 @ X=250, 110 km/h)</div>
        <div className="text-emerald-400">[{state.simulationTime}] TELEMETRY_PING: WORKER_LOCATION_UPDATE (Ramesh Kumar @ X=450, GPS ±4.2m)</div>
        {state.alerts.map((a) => (
          <div key={a.id} className="text-amber-400">
            [{a.createdAt}] ALERT_STATE_CHANGE: {a.state} for {a.workerName} (TTD: {a.timeToDangerSeconds}s)
          </div>
        ))}
      </div>
    </div>
  );
};
