import React from 'react';
import { SimulationState } from '../../types/simulation';
import { ShieldAlert, AlertCircle, MapPin, Calendar } from 'lucide-react';

interface NearMissViewProps {
  state: SimulationState;
}

export const NearMissView: React.FC<NearMissViewProps> = ({ state }) => {
  return (
    <div className="space-y-6">
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">NEAR-MISS INTELLIGENCE & HEATMAPS</h2>
            <p className="text-xs text-slate-400">Automated spatial clearance breach detection (&lt; 3.0m)</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-amber-500/20 text-amber-300 rounded-lg text-xs font-mono font-bold">
          {state.nearMisses.length} INCIDENTS RECORDED
        </span>
      </div>

      {/* Near-Miss Timeline & List */}
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-4 shadow-xl">
        <h3 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
          RECENT NEAR-MISS INCIDENT RECORDS
        </h3>

        <div className="space-y-3">
          {state.nearMisses.map((nm) => (
            <div key={nm.id} className="p-4 bg-[#090D16] border border-slate-800 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 rounded">
                    {nm.severity} SEVERITY
                  </span>
                  <span className="text-xs font-bold text-slate-100">{nm.id}</span>
                </div>
                <div className="flex items-center space-x-1 text-[11px] font-mono text-slate-400">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>{nm.occurredAt}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-2 text-xs font-mono text-slate-300 mt-1">
                <div>Worker: <span className="text-cyan-300 font-bold">{nm.workerName}</span></div>
                <div>Train: <span className="text-blue-300 font-bold">{nm.trainId} ({nm.trainSpeedKmh} km/h)</span></div>
                <div>Min Clearance: <span className="text-amber-400 font-bold">{nm.minSpatialClearanceMeters}m</span></div>
                <div>TTD at Ack: <span className="text-emerald-400 font-bold">{nm.ttdAtAckSeconds}s</span></div>
              </div>

              <div className="text-xs text-slate-400 font-mono mt-1">
                Contributing Factors: {nm.contributingFactors.join(' • ')}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
