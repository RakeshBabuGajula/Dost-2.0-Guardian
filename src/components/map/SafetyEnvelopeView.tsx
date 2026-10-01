import React from 'react';
import { Worker, Train } from '../../types/railway';
import { Shield, ArrowRight, Zap, Info } from 'lucide-react';

interface SafetyEnvelopeViewProps {
  worker: Worker;
  train: Train;
}

export const SafetyEnvelopeView: React.FC<SafetyEnvelopeViewProps> = ({ worker, train }) => {
  const trainSpeedMps = (train.speedKmh * 1000) / 3600;
  const reactionBufferMeters = Math.round(trainSpeedMps * worker.envelope.reactionTimeSeconds);
  const totalBufferMeters = reactionBufferMeters + Math.round(worker.envelope.clearanceBufferMeters) + Math.round(worker.envelope.gpsUncertaintyBufferMeters);

  return (
    <div className="bg-[#121826] border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 font-mono">DYNAMIC SAFETY ENVELOPE COMPUTATION</h3>
            <p className="text-xs text-slate-400">Deterministic Spatial Warning Buffer Calculation</p>
          </div>
        </div>
        <span className="px-2.5 py-1 text-[11px] font-mono bg-slate-900 border border-slate-800 text-cyan-400 rounded-lg">
          [PROPOSED DESIGN]
        </span>
      </div>

      {/* Vector Pipeline Visualization */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-center bg-[#090D16] p-4 rounded-xl border border-slate-800/80 mb-4">
        {/* Step 1: Train Vector */}
        <div className="p-3 bg-[#121826] rounded-lg border border-slate-800 text-center">
          <span className="text-[10px] font-mono text-slate-400 uppercase">1. Train Velocity</span>
          <div className="text-lg font-bold font-mono text-cyan-400 mt-1">{train.speedKmh} km/h</div>
          <span className="text-[11px] text-slate-400">({trainSpeedMps.toFixed(1)} m/s)</span>
        </div>

        <ArrowRight className="hidden md:block w-5 h-5 text-slate-600 justify-self-center" />

        {/* Step 2: Reaction Time Buffer */}
        <div className="p-3 bg-[#121826] rounded-lg border border-slate-800 text-center">
          <span className="text-[10px] font-mono text-slate-400 uppercase">2. Reaction Buffer</span>
          <div className="text-lg font-bold font-mono text-amber-400 mt-1">{reactionBufferMeters} m</div>
          <span className="text-[11px] text-slate-400">(10s Perception Time)</span>
        </div>

        <ArrowRight className="hidden md:block w-5 h-5 text-slate-600 justify-self-center" />

        {/* Step 3: Total Dynamic Envelope */}
        <div className="p-3 bg-cyan-950/30 rounded-lg border border-cyan-500/40 text-center">
          <span className="text-[10px] font-mono text-cyan-300 uppercase font-semibold">3. Dynamic Envelope Radius</span>
          <div className="text-xl font-bold font-mono text-cyan-300 mt-1">{totalBufferMeters} m</div>
          <span className="text-[11px] text-cyan-400 font-mono">Calculated Buffer</span>
        </div>
      </div>

      {/* Mathematical Breakdown Formula */}
      <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800 text-xs font-mono space-y-2 text-slate-300">
        <div className="flex items-center space-x-2 text-cyan-400 font-semibold">
          <Zap className="w-4 h-4" />
          <span>Formula: D_buffer = (v_train × t_reaction) + D_clearance + D_gps_uncertainty</span>
        </div>
        <div className="text-slate-400 text-[11px] leading-relaxed">
          - <b>v_train</b>: Reported ground speed ({train.speedKmh} km/h = {trainSpeedMps.toFixed(1)} m/s)<br />
          - <b>t_reaction</b>: 10 seconds perception & evacuation clearance buffer<br />
          - <b>D_clearance</b>: 3.0 meters standard track clearance line<br />
          - <b>D_gps_uncertainty</b>: {worker.envelope.gpsUncertaintyBufferMeters.toFixed(1)} meters (GNSS accuracy callback)
        </div>
      </div>

      <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 font-mono">
        <span className="flex items-center space-x-1">
          <Info className="w-3.5 h-3.5 text-slate-400" />
          <span>Values marked as CONFIGURABLE / SIMULATION VALUE</span>
        </span>
        <span className="text-emerald-400 font-medium">100% Deterministic Engine Rule</span>
      </div>
    </div>
  );
};
