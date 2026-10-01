import React from 'react';
import { Alert } from '../../types/safety';
import { StatusBadge } from '../common/StatusBadge';
import { Bell, CheckCircle, ShieldAlert } from 'lucide-react';

interface AlertQueuePanelProps {
  alerts: Alert[];
  onAcknowledge: (alertId: string, workerId: string) => void;
}

export const AlertQueuePanel: React.FC<AlertQueuePanelProps> = ({ alerts, onAcknowledge }) => {
  return (
    <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 flex flex-col h-full shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <div className="flex items-center space-x-2">
          <Bell className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-mono font-bold text-slate-100 uppercase tracking-wider">LIVE ALERT QUEUE</span>
        </div>
        <span className="px-2 py-0.5 text-[10px] font-mono bg-cyan-500/20 text-cyan-300 rounded-full font-bold">
          {alerts.filter((a) => !a.isAcknowledged).length} UNACKNOWLEDGED
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {alerts.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-400 font-mono">
            <CheckCircle className="w-6 h-6 text-emerald-400 mx-auto mb-2 opacity-60" />
            No active alerts in queue
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-3 rounded-xl border transition-all ${
                alert.isAcknowledged
                  ? 'bg-slate-900/40 border-slate-800 text-slate-400'
                  : alert.state === 'CRITICAL' || alert.state === 'EMERGENCY'
                  ? 'bg-red-950/30 border-red-500/50 shadow-md shadow-red-950/30'
                  : 'bg-slate-900 border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <StatusBadge status={alert.state} size="sm" />
                <span className="text-[10px] font-mono text-slate-400">{alert.createdAt}</span>
              </div>

              <div className="text-xs font-bold text-slate-200">{alert.workerName}</div>
              <div className="text-[11px] font-mono text-slate-400">
                {alert.trainName} ({alert.trainId}) | TTD: <span className="text-red-400 font-bold">{alert.timeToDangerSeconds}s</span>
              </div>

              {!alert.isAcknowledged && (
                <div className="mt-2.5 flex items-center justify-between pt-2 border-t border-slate-800">
                  <span className="text-[10px] font-mono text-amber-400">{alert.escalationTier}</span>
                  <button
                    onClick={() => onAcknowledge(alert.id, alert.workerId)}
                    className="px-2.5 py-1 text-[10px] font-mono font-bold bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition"
                  >
                    OVERRIDE ACK
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
