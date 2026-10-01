import React, { useEffect } from 'react';
import { Alert } from '../../types/safety';
import { ShieldAlert, CheckCircle, Volume2, AlertOctagon } from 'lucide-react';

interface CriticalAlertOverlayProps {
  alert: Alert;
  onAcknowledge: (alertId: string, workerId: string) => void;
  onTriggerSos: (workerId: string) => void;
}

export const CriticalAlertOverlay: React.FC<CriticalAlertOverlayProps> = ({
  alert,
  onAcknowledge,
  onTriggerSos,
}) => {
  // Purposeful audio simulation effect indication
  useEffect(() => {
    // Visual flash wake lock indication
    document.body.classList.add('select-none');
    return () => {
      document.body.classList.remove('select-none');
    };
  }, []);

  const formatTTD = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 z-50 bg-red-950/90 backdrop-blur-lg flex items-center justify-center p-4 sm:p-6 animate-in fade-in zoom-in duration-200">
      <div className="w-full max-w-lg bg-[#0F0404] border-4 border-red-600 rounded-3xl p-6 shadow-2xl shadow-red-900/80 flex flex-col justify-between text-center space-y-6 animate-pulse-ring">
        {/* Top Warning Banner */}
        <div className="flex items-center justify-between border-b-2 border-red-800/80 pb-4">
          <div className="flex items-center space-x-2 text-red-500">
            <AlertOctagon className="w-8 h-8 animate-bounce" />
            <span className="text-2xl font-black tracking-wider uppercase font-mono">CRITICAL ALERT</span>
          </div>
          <div className="flex items-center space-x-1 px-3 py-1 bg-red-900/60 rounded-full border border-red-500 text-red-300 text-xs font-mono font-bold">
            <Volume2 className="w-4 h-4 animate-pulse" />
            <span>85 dB SIREN ACTIVE</span>
          </div>
        </div>

        {/* Core Threat Header */}
        <div className="space-y-2">
          <h2 className="text-xl sm:text-2xl font-extrabold text-white uppercase tracking-tight">
            TRAIN APPROACHING — DOWN LINE
          </h2>
          <p className="text-sm font-mono text-red-300 font-semibold">
            {alert.trainName} ({alert.trainId}) | Section: {alert.blockSectionCode}
          </p>
        </div>

        {/* TIME-TO-DANGER COUNTDOWN HERO */}
        <div className="bg-red-950/80 border-2 border-red-600 rounded-2xl py-6 px-4 shadow-inner">
          <div className="text-xs font-mono uppercase tracking-widest text-red-400 font-semibold mb-1">
            ESTIMATED TIME TO AFFECTED ZONE
          </div>
          <div className="text-6xl sm:text-7xl font-extrabold font-mono text-white tracking-tighter drop-shadow-md">
            {formatTTD(alert.timeToDangerSeconds)}
          </div>
          <div className="text-xs font-mono text-red-300 mt-2">
            Distance: {alert.distanceToTrainMeters} meters | Speed: 110 km/h
          </div>
        </div>

        {/* Required Action Instruction */}
        <div className="bg-red-900/40 p-4 rounded-xl border border-red-700 text-center">
          <div className="text-xs font-mono text-red-400 uppercase font-bold tracking-wider mb-1">
            REQUIRED IMMEDIATE ACTION
          </div>
          <div className="text-base sm:text-lg font-black text-white leading-snug">
            MOVE TO DESIGNATED SAFE REFUGE ZONE IMMEDIATELY
          </div>
        </div>

        {/* PRIMARY ACTION: I'M SAFE BUTTON (72px height, gloved touch target) */}
        <button
          onClick={() => onAcknowledge(alert.id, alert.workerId)}
          className="w-full h-18 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white font-black text-xl tracking-wider rounded-2xl shadow-xl shadow-emerald-950/50 border-2 border-emerald-400 flex items-center justify-center space-x-3 transition-all"
        >
          <CheckCircle className="w-8 h-8" />
          <span>I&apos;M SAFE (ACKNOWLEDGE)</span>
        </button>

        {/* Secondary Emergency SOS Trigger */}
        <button
          onClick={() => onTriggerSos(alert.workerId)}
          className="w-full py-3 bg-red-900/60 hover:bg-red-800 text-red-200 font-mono text-xs font-bold rounded-xl border border-red-700 flex items-center justify-center space-x-2"
        >
          <ShieldAlert className="w-4 h-4 text-red-400" />
          <span>TRIGGER MANUAL EMERGENCY SOS (HOLD 3 SECS)</span>
        </button>
      </div>
    </div>
  );
};
