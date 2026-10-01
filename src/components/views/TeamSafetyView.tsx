import React from 'react';
import { SimulationState } from '../../types/simulation';
import { StatusBadge } from '../common/StatusBadge';
import { Users, Shield, CheckCircle, Smartphone } from 'lucide-react';

interface TeamSafetyViewProps {
  state: SimulationState;
  onAcknowledgeAlert: (alertId: string, workerId: string) => void;
}

export const TeamSafetyView: React.FC<TeamSafetyViewProps> = ({ state, onAcknowledgeAlert }) => {
  return (
    <div className="space-y-6">
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
            <Users className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">TEAM SAFETY ACCOUNTABILITY MATRIX</h2>
            <p className="text-xs text-slate-400">Real-time gang roster monitoring & supervisor control</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-cyan-500/20 text-cyan-300 rounded-lg text-xs font-mono font-bold">
          GANG 04 — CHENNAI DIVISION
        </span>
      </div>

      {/* Roster Table */}
      <div className="bg-[#121826] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#090D16] border-b border-slate-800 text-slate-400 font-mono uppercase text-[10px]">
              <tr>
                <th className="px-4 py-3">Worker / Designation</th>
                <th className="px-4 py-3">Safety Status</th>
                <th className="px-4 py-3">Block Section</th>
                <th className="px-4 py-3">Battery</th>
                <th className="px-4 py-3">Network Link</th>
                <th className="px-4 py-3">GPS Accuracy</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80 text-slate-200">
              {state.workers.map((worker) => (
                <tr key={worker.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-4 py-3 font-medium">
                    <div className="font-bold text-slate-100">{worker.name}</div>
                    <div className="text-[10px] font-mono text-slate-400">{worker.role} ({worker.id})</div>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge status={worker.status} size="sm" />
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-300">{worker.currentBlockSection}</td>
                  <td className="px-4 py-3 font-mono">
                    <span className={worker.batteryLevel < 20 ? 'text-amber-400 font-bold' : 'text-slate-300'}>
                      {worker.batteryLevel}%
                    </span>
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-300">{worker.networkState}</td>
                  <td className="px-4 py-3 font-mono text-slate-300">±{worker.gpsAccuracyMeters}m</td>
                  <td className="px-4 py-3 text-right">
                    {worker.unacknowledgedAlertId ? (
                      <button
                        onClick={() => onAcknowledgeAlert(worker.unacknowledgedAlertId!, worker.id)}
                        className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-[10px] font-bold rounded-lg transition"
                      >
                        OVERRIDE ACK
                      </button>
                    ) : (
                      <span className="text-[10px] font-mono text-slate-500">Normal</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
