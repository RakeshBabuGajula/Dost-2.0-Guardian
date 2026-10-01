import React from 'react';
import { Worker, Train, WorkZone, BlockSection } from '../../types/railway';
import { Shield, MapPin, Compass, Navigation, Radio, X } from 'lucide-react';

interface SpatialContextDrawerProps {
  selectedWorker?: Worker | null;
  selectedTrain?: Train | null;
  selectedWorkZone?: WorkZone | null;
  onClose: () => void;
}

export const SpatialContextDrawer: React.FC<SpatialContextDrawerProps> = ({
  selectedWorker,
  selectedTrain,
  selectedWorkZone,
  onClose,
}) => {
  if (!selectedWorker && !selectedTrain && !selectedWorkZone) return null;

  return (
    <div className="absolute right-4 top-16 z-20 w-80 bg-[#0F172A]/95 border border-slate-700/80 rounded-2xl p-4 shadow-2xl backdrop-blur-md text-slate-100 scanline-effect animate-in fade-in slide-in-from-right-4 duration-200">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
        <div className="flex items-center space-x-2">
          <MapPin className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-mono font-bold tracking-wider text-cyan-300">
            SPATIAL GEOSPATIAL CONTEXT
          </span>
        </div>
        <button onClick={onClose} className="p-1 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-slate-200 transition">
          <X className="w-4 h-4" />
        </button>
      </div>

      {selectedWorker && (
        <div className="space-y-2.5 text-xs font-mono">
          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Worker ID / Name:</span>
            <span className="font-bold text-cyan-400">{selectedWorker.id} ({selectedWorker.name.split(' ')[0]})</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">WGS84 Coordinates:</span>
            <span className="text-emerald-400">
              {selectedWorker.position.lat ?? 13.0823}° N, {selectedWorker.position.lng ?? 80.2750}° E
            </span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Block Section:</span>
            <span className="text-amber-400">{selectedWorker.currentBlockSection}</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Nearest Refuge Niche:</span>
            <span className="text-emerald-300">REFUGE-MAS-101 (42m)</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">GPS Accuracy:</span>
            <span className="text-slate-300">±{selectedWorker.gpsAccuracyMeters} meters</span>
          </div>

          <div className="p-2 rounded-lg bg-cyan-950/40 border border-cyan-800/40 text-[10px] text-cyan-300 leading-relaxed">
            [SPATIAL ENRICHMENT]: Informational spatial proximity data only. Does not constitute a certified railway safety decision.
          </div>
        </div>
      )}

      {selectedTrain && (
        <div className="space-y-2.5 text-xs font-mono">
          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Train ID / Number:</span>
            <span className="font-bold text-sky-400">{selectedTrain.id} ({selectedTrain.number})</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Track Line:</span>
            <span className="text-cyan-300">{selectedTrain.line} ({selectedTrain.direction})</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Speed / Heading:</span>
            <span className="text-rose-400">{selectedTrain.speedKmh} km/h (90.0° East)</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Containing Block:</span>
            <span className="text-amber-400">{selectedTrain.currentBlockSection}</span>
          </div>

          <div className="p-2 rounded-lg bg-cyan-950/40 border border-cyan-800/40 text-[10px] text-cyan-300 leading-relaxed">
            [SPATIAL ENRICHMENT]: Track telemetry vector. Informational spatial query parameter.
          </div>
        </div>
      )}

      {selectedWorkZone && (
        <div className="space-y-2.5 text-xs font-mono">
          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Work Zone Code:</span>
            <span className="font-bold text-emerald-400">{selectedWorkZone.code}</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Block Section:</span>
            <span className="text-amber-400">{selectedWorkZone.blockSectionCode}</span>
          </div>

          <div className="flex items-center justify-between bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span className="text-slate-400">Zone Polygon Status:</span>
            <span className="text-emerald-300">{selectedWorkZone.status}</span>
          </div>
        </div>
      )}
    </div>
  );
};
