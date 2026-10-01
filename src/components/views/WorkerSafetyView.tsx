import React from 'react';
import { SimulationState } from '../../types/simulation';
import { StatusBadge } from '../common/StatusBadge';
import { CheckCircle, ShieldAlert, Wifi, Battery, MapPin, Volume2 } from 'lucide-react';

interface WorkerSafetyViewProps {
  state: SimulationState;
  onAcknowledgeAlert: (alertId: string, workerId: string) => void;
  onTriggerSos: (workerId: string) => void;
}

export const WorkerSafetyView: React.FC<WorkerSafetyViewProps> = ({
  state,
  onAcknowledgeAlert,
  onTriggerSos,
}) => {
  const worker = state.workers[0]; // Ramesh Kumar
  const activeAlert = state.alerts.find((a) => a.workerId === worker?.id && !a.isAcknowledged);

  if (!worker) return null;

  return (
    <div className="max-w-md mx-auto bg-[#090D16] border-2 border-slate-800 rounded-3xl p-5 shadow-2xl space-y-6">
      {/* Mobile Device Header Bar */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-xs font-mono font-bold text-slate-200">DOST GUARDIAN MOBILE</span>
        </div>
        <div className="flex items-center space-x-3 text-xs font-mono text-slate-400">
          <span className="flex items-center space-x-1">
            <Wifi className="w-3.5 h-3.5 text-emerald-400" />
            <span>4G</span>
          </span>
          <span className="flex items-center space-x-1">
            <Battery className="w-3.5 h-3.5 text-emerald-400" />
            <span>{worker.batteryLevel}%</span>
          </span>
        </div>
      </div>

      {/* Worker Profile Summary */}
      <div className="bg-[#121826] p-4 rounded-2xl border border-slate-800 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono text-slate-400 uppercase">Field Maintainer</span>
          <StatusBadge status={worker.status} size="md" />
        </div>
        <h3 className="text-lg font-bold text-slate-100">{worker.name}</h3>
        <div className="flex items-center space-x-1 text-xs text-slate-400 font-mono">
          <MapPin className="w-3.5 h-3.5 text-cyan-400" />
          <span>Work Zone: {worker.currentBlockSection}</span>
        </div>
      </div>

      {/* Active Safety Status Card */}
      {activeAlert ? (
        <div className="bg-red-950/40 border-2 border-red-600 rounded-2xl p-5 text-center space-y-4 animate-pulse-ring">
          <div className="flex items-center justify-center space-x-2 text-red-400 font-mono font-bold text-xs uppercase">
            <Volume2 className="w-4 h-4 animate-bounce" />
            <span>CRITICAL WARNING ACTIVE</span>
          </div>

          <div className="text-4xl font-extrabold font-mono text-white tracking-tight">
            00:{activeAlert.timeToDangerSeconds.toString().padStart(2, '0')}
          </div>

          <div className="text-xs font-mono text-red-300 font-semibold">
            {activeAlert.trainName} ({activeAlert.trainId}) APPROACHING
          </div>

          <button
            onClick={() => onAcknowledgeAlert(activeAlert.id, worker.id)}
            className="w-full h-16 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white font-black text-lg rounded-xl shadow-lg border border-emerald-400 flex items-center justify-center space-x-2 transition"
          >
            <CheckCircle className="w-6 h-6" />
            <span>I&apos;M SAFE (ACKNOWLEDGE)</span>
          </button>
        </div>
      ) : (
        <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-2xl p-6 text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto">
            <CheckCircle className="w-7 h-7" />
          </div>
          <h4 className="text-base font-bold text-emerald-300">PROTECTION ACTIVE — TRACK SAFE</h4>
          <p className="text-xs text-slate-400">
            Dynamic Safety Envelope active. Automatic audio-visual alert will trigger if train enters section.
          </p>
        </div>
      )}

      {/* Emergency SOS Trigger */}
      <button
        onClick={() => onTriggerSos(worker.id)}
        className="w-full py-3.5 bg-red-950/60 hover:bg-red-900 text-red-300 text-xs font-mono font-bold rounded-xl border border-red-800 flex items-center justify-center space-x-2 transition"
      >
        <ShieldAlert className="w-4 h-4 text-red-400" />
        <span>TRIGGER EMERGENCY SOS</span>
      </button>

      <div className="text-center text-[10px] font-mono text-slate-500">
        GPS Accuracy: ±{worker.gpsAccuracyMeters}m | Server Ping: {worker.lastPingSecondsAgo}s ago
      </div>
    </div>
  );
};
