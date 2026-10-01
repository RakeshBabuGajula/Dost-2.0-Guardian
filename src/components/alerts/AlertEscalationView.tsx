import React from 'react';
import { Alert } from '../../types/safety';
import { ArrowRight, AlertTriangle, ShieldAlert, Radio } from 'lucide-react';

interface AlertEscalationViewProps {
  alert?: Alert;
}

export const AlertEscalationView: React.FC<AlertEscalationViewProps> = ({ alert }) => {
  const steps = [
    { title: '1. TRAIN DETECTED', desc: 'Signaling feed ingress', active: true, completed: true },
    { title: '2. TTD COMPUTED', desc: 'Safety Engine calculation', active: true, completed: true },
    { title: '3. WORKER ALERTED', desc: 'Local Siren (T0 = 0s)', active: true, completed: alert ? alert.timeToDangerSeconds <= 90 : false },
    {
      title: '4. SUPERVISOR TIER-1', desc: 'Unack timer T1 = 10s',
      active: alert?.escalationTier === 'TIER_1_SUPERVISOR' || alert?.escalationTier === 'TIER_2_SECTION_ENG' || alert?.escalationTier === 'TIER_3_CONTROL_ROOM',
      completed: alert?.escalationTier === 'TIER_2_SECTION_ENG' || alert?.escalationTier === 'TIER_3_CONTROL_ROOM',
    },
    {
      title: '5. CONTROL ROOM TIER-3', desc: 'Emergency broadcast T2 = 20s',
      active: alert?.escalationTier === 'TIER_3_CONTROL_ROOM',
      completed: alert?.escalationTier === 'TIER_3_CONTROL_ROOM',
    },
  ];

  return (
    <div className="bg-[#121826] border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-orange-500/20 text-orange-400">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 font-mono">MULTI-TIER ESCALATION LIFECYCLE STEPPER</h3>
            <p className="text-xs text-slate-400">Automated Hierarchy Escalation Protocol</p>
          </div>
        </div>
        <span className="px-2.5 py-1 text-[11px] font-mono bg-slate-900 border border-slate-800 text-orange-400 rounded-lg">
          [PROPOSED DESIGN]
        </span>
      </div>

      {/* Stepper Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        {steps.map((step, i) => (
          <div
            key={i}
            className={`p-3 rounded-xl border transition-all ${
              step.active
                ? step.completed
                  ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
                  : 'bg-red-950/30 border-red-500/50 text-red-300 animate-pulse'
                : 'bg-slate-900/40 border-slate-800 text-slate-400'
            }`}
          >
            <div className="text-[10px] font-mono font-bold uppercase tracking-wider">{step.title}</div>
            <div className="text-[11px] text-slate-400 mt-1">{step.desc}</div>
          </div>
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between text-[11px] font-mono text-slate-400 bg-slate-900/50 p-2.5 rounded-lg border border-slate-800">
        <span className="flex items-center space-x-1.5">
          <Radio className="w-3.5 h-3.5 text-cyan-400" />
          <span>Active Policy: T0 (Worker) → T1 (+10s Supervisor) → T2/T3 (+20s Control Room)</span>
        </span>
        <span className="text-slate-400">Configurable Policy Parameters</span>
      </div>
    </div>
  );
};
