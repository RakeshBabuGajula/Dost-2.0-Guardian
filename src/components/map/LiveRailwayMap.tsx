import React, { useState } from 'react';
import { Worker, Train, WorkZone, BlockSection } from '../../types/railway';
import { StatusBadge } from '../common/StatusBadge';
import { Shield, Eye, Layers } from 'lucide-react';

import { SpatialContextDrawer } from './SpatialContextDrawer';

interface LiveRailwayMapProps {
  workers: Worker[];
  trains: Train[];
  workZones: WorkZone[];
  blockSections: BlockSection[];
  onSelectWorker?: (worker: Worker) => void;
  onSelectTrain?: (train: Train) => void;
}

export const LiveRailwayMap: React.FC<LiveRailwayMapProps> = ({
  workers,
  trains,
  workZones,
  onSelectWorker,
  onSelectTrain,
}) => {
  const [showEnvelopes, setShowEnvelopes] = useState(true);
  const [showRefugeZones, setShowRefugeZones] = useState(true);
  const [selectedWorkerObj, setSelectedWorkerObj] = useState<Worker | null>(null);
  const [selectedTrainObj, setSelectedTrainObj] = useState<Train | null>(null);
  const [selectedWorkZoneObj, setSelectedWorkZoneObj] = useState<WorkZone | null>(null);
  const [selectedEntity, setSelectedEntity] = useState<string | null>(null);

  return (
    <div className="relative bg-[#090D16] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl scanline-effect min-h-[420px] flex flex-col justify-between p-4">
      {/* Map Header Overlay */}
      <div className="flex items-center justify-between z-10 bg-[#121826]/80 backdrop-blur-md px-4 py-2.5 rounded-xl border border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="p-1.5 rounded-lg bg-cyan-500/20 text-cyan-400">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <span className="text-xs font-mono font-bold text-slate-100 tracking-wider">MAS-AJJ SECTION GIS MAP</span>
            <span className="text-[10px] text-cyan-400 font-mono block">LIVE SIMULATION TRACK RADAR</span>
          </div>
        </div>

        {/* Layer Controls */}
        <div className="flex items-center space-x-2 text-xs font-mono">
          <button
            onClick={() => setShowEnvelopes(!showEnvelopes)}
            className={`px-2.5 py-1 rounded-lg border transition ${
              showEnvelopes ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40' : 'text-slate-500 border-slate-800'
            }`}
          >
            Safety Envelopes
          </button>
          <button
            onClick={() => setShowRefugeZones(!showRefugeZones)}
            className={`px-2.5 py-1 rounded-lg border transition ${
              showRefugeZones ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' : 'text-slate-500 border-slate-800'
            }`}
          >
            Refuge Niche
          </button>
        </div>
      </div>

      {/* SVG Canvas for Track Visualization */}
      <div className="my-4 relative w-full h-[320px] bg-[#0B101D] rounded-xl border border-slate-800/80 overflow-hidden flex items-center justify-center">
        <svg viewBox="0 0 1000 400" className="w-full h-full">
          <defs>
            {/* Track pattern */}
            <pattern id="sleeperPattern" width="10" height="20" patternUnits="userSpaceOnUse">
              <line x1="5" y1="0" x2="5" y2="20" stroke="#1E293B" strokeWidth="2" />
            </pattern>
            {/* Dynamic Danger Gradient */}
            <radialGradient id="dangerGradient">
              <stop offset="0%" stopColor="#EF4444" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#EF4444" stopOpacity="0" />
            </radialGradient>
          </defs>

          {/* Grid lines */}
          <g opacity="0.15">
            {Array.from({ length: 20 }).map((_, i) => (
              <line key={`v-${i}`} x1={i * 50} y1="0" x2={i * 50} y2="400" stroke="#64748B" strokeWidth="1" strokeDasharray="2,4" />
            ))}
            {Array.from({ length: 8 }).map((_, i) => (
              <line key={`h-${i}`} x1="0" y1={i * 50} x2="1000" y2={i * 50} stroke="#64748B" strokeWidth="1" strokeDasharray="2,4" />
            ))}
          </g>

          {/* Block Section Markers & Labels */}
          <g>
            <rect x="20" y="20" width="440" height="360" fill="none" stroke="#1E293B" strokeWidth="1" strokeDasharray="4,4" />
            <text x="30" y="40" fill="#475569" fontSize="10" fontFamily="monospace">BLOCK SECTION: MAS-AJJ-DOWN-120</text>

            <rect x="500" y="20" width="480" height="360" fill="none" stroke="#1E293B" strokeWidth="1" strokeDasharray="4,4" />
            <text x="510" y="40" fill="#475569" fontSize="10" fontFamily="monospace">BLOCK SECTION: MAS-AJJ-UP-122</text>
          </g>

          {/* RAILWAY TRACK 1: DOWN LINE (Y = 140) */}
          <g>
            {/* Ballast / Track Base */}
            <line x1="30" y1="140" x2="970" y2="140" stroke="#1E2A3A" strokeWidth="20" strokeLinecap="round" />
            <line x1="30" y1="134" x2="970" y2="134" stroke="#0284C7" strokeWidth="2" opacity="0.6" />
            <line x1="30" y1="146" x2="970" y2="146" stroke="#0284C7" strokeWidth="2" opacity="0.6" />
            <text x="40" y="120" fill="#38BDF8" fontSize="11" fontWeight="bold" fontFamily="monospace">DOWN LINE (WESTBOUND)</text>
          </g>

          {/* RAILWAY TRACK 2: UP LINE (Y = 260) */}
          <g>
            <line x1="30" y1="260" x2="970" y2="260" stroke="#1E2A3A" strokeWidth="20" strokeLinecap="round" />
            <line x1="30" y1="254" x2="970" y2="254" stroke="#06B6D4" strokeWidth="2" opacity="0.6" />
            <line x1="30" y1="266" x2="970" y2="266" stroke="#06B6D4" strokeWidth="2" opacity="0.6" />
            <text x="40" y="290" fill="#22D3EE" fontSize="11" fontWeight="bold" fontFamily="monospace">UP LINE (EASTBOUND)</text>
          </g>

          {/* WORK ZONES HIGHLIGHT (BZ-MAS-120) */}
          {workZones.map((wz) => (
            <g key={wz.id}>
              <rect
                x={wz.trackSegmentRange.startX}
                y="110"
                width={wz.trackSegmentRange.endX - wz.trackSegmentRange.startX}
                height="60"
                fill="rgba(16, 185, 129, 0.08)"
                stroke="#10B981"
                strokeWidth="1.5"
                strokeDasharray="4,4"
                rx="6"
              />
              <text
                x={wz.trackSegmentRange.startX + 10}
                y="100"
                fill="#10B981"
                fontSize="10"
                fontWeight="bold"
                fontFamily="monospace"
              >
                WORK ZONE: {wz.code}
              </text>
            </g>
          ))}

          {/* SAFE REFUGE ZONES */}
          {showRefugeZones && (
            <g>
              <rect x="440" y="75" width="80" height="25" fill="#10B981" fillOpacity="0.2" stroke="#10B981" strokeWidth="1" rx="4" />
              <text x="450" y="91" fill="#10B981" fontSize="9" fontWeight="bold" fontFamily="monospace">SAFE REFUGE</text>

              <rect x="810" y="305" width="80" height="25" fill="#10B981" fillOpacity="0.2" stroke="#10B981" strokeWidth="1" rx="4" />
              <text x="820" y="321" fill="#10B981" fontSize="9" fontWeight="bold" fontFamily="monospace">SAFE REFUGE</text>
            </g>
          )}

          {/* DYNAMIC SAFETY ENVELOPES & WORKERS */}
          {workers.map((worker) => {
            const isSelected = selectedEntity === worker.id;
            const envelopeRadius = worker.envelope.radiusMeters / 10; // scale meters to map units
            const isCritical = worker.status === 'CRITICAL' || worker.status === 'EMERGENCY';

            return (
              <g key={worker.id} className="cursor-pointer" onClick={() => { setSelectedEntity(worker.id); setSelectedWorkerObj(worker); setSelectedTrainObj(null); setSelectedWorkZoneObj(null); onSelectWorker?.(worker); }}>
                {/* Dynamic Safety Envelope Ring */}
                {showEnvelopes && (
                  <circle
                    cx={worker.position.x}
                    cy={worker.position.y}
                    r={envelopeRadius}
                    fill={isCritical ? 'url(#dangerGradient)' : 'rgba(6, 182, 212, 0.06)'}
                    stroke={
                      isCritical
                        ? '#EF4444'
                        : worker.status === 'WARNING'
                        ? '#F97316'
                        : worker.status === 'CAUTION'
                        ? '#F59E0B'
                        : '#06B6D4'
                    }
                    strokeWidth={worker.envelope.isExpandedDueToGps ? '2.5' : '1.5'}
                    strokeDasharray={worker.envelope.isExpandedDueToGps ? '6,3' : undefined}
                    className={isCritical ? 'animate-pulse' : undefined}
                  />
                )}

                {/* Worker Marker Dot */}
                <circle
                  cx={worker.position.x}
                  cy={worker.position.y}
                  r="8"
                  fill={
                    isCritical
                      ? '#EF4444'
                      : worker.status === 'WARNING'
                      ? '#F97316'
                      : worker.status === 'CAUTION'
                      ? '#F59E0B'
                      : worker.status === 'DEGRADED_NETWORK'
                      ? '#F97316'
                      : '#10B981'
                  }
                  stroke="#FFFFFF"
                  strokeWidth={isSelected ? '3' : '1.5'}
                />

                {/* Worker Label */}
                <text
                  x={worker.position.x}
                  y={worker.position.y - 14}
                  textAnchor="middle"
                  fill="#F8FAFC"
                  fontSize="10"
                  fontWeight="bold"
                  fontFamily="monospace"
                >
                  {worker.name.split(' ')[0]}
                </text>
              </g>
            );
          })}

          {/* TRAIN VECTORS */}
          {trains.map((train) => {
            const isSelected = selectedEntity === train.id;
            return (
              <g key={train.id} className="cursor-pointer" onClick={() => { setSelectedEntity(train.id); setSelectedTrainObj(train); setSelectedWorkerObj(null); setSelectedWorkZoneObj(null); onSelectTrain?.(train); }}>
                {/* Projected Stopping Vector */}
                <line
                  x1={train.positionX}
                  y1={train.positionY}
                  x2={train.positionX + (train.direction === 'WESTBOUND' ? 120 : -120)}
                  y2={train.positionY}
                  stroke="#EF4444"
                  strokeWidth="2"
                  strokeDasharray="4,4"
                />

                {/* Train Body Rect */}
                <rect
                  x={train.positionX - 25}
                  y={train.positionY - 12}
                  width="50"
                  height="24"
                  fill="#0284C7"
                  stroke="#FFFFFF"
                  strokeWidth={isSelected ? '2.5' : '1.5'}
                  rx="4"
                />

                {/* Direction Arrow */}
                <polygon
                  points={
                    train.direction === 'WESTBOUND'
                      ? `${train.positionX + 25},${train.positionY - 6} ${train.positionX + 33},${train.positionY} ${train.positionX + 25},${train.positionY + 6}`
                      : `${train.positionX - 25},${train.positionY - 6} ${train.positionX - 33},${train.positionY} ${train.positionX - 25},${train.positionY + 6}`
                  }
                  fill="#38BDF8"
                />

                {/* Train Code Label */}
                <text
                  x={train.positionX}
                  y={train.positionY + 4}
                  textAnchor="middle"
                  fill="#FFFFFF"
                  fontSize="9"
                  fontWeight="bold"
                  fontFamily="monospace"
                >
                  {train.number}
                </text>

                {/* Speed tag */}
                <text
                  x={train.positionX}
                  y={train.positionY - 18}
                  textAnchor="middle"
                  fill="#38BDF8"
                  fontSize="9"
                  fontFamily="monospace"
                >
                  {train.speedKmh} km/h
                </text>
              </g>
            );
          })}
        </svg>

        {/* Render Spatial Context Drawer */}
        <SpatialContextDrawer
          selectedWorker={selectedWorkerObj}
          selectedTrain={selectedTrainObj}
          selectedWorkZone={selectedWorkZoneObj}
          onClose={() => {
            setSelectedWorkerObj(null);
            setSelectedTrainObj(null);
            setSelectedWorkZoneObj(null);
            setSelectedEntity(null);
          }}
        />
      </div>


      {/* Map Footer Information Bar */}
      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 bg-[#121826]/80 px-4 py-2 rounded-xl border border-slate-800">
        <div className="flex items-center space-x-4">
          <span className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
            <span>Workers Active: {workers.length}</span>
          </span>
          <span className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-500 inline-block"></span>
            <span>Trains Tracked: {trains.length}</span>
          </span>
        </div>
        <div className="text-slate-400">
          Click any entity marker to view dynamic telemetry
        </div>
      </div>
    </div>
  );
};
