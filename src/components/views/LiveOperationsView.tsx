import React from 'react';
import { SimulationState } from '../../types/simulation';
import { LiveRailwayMap } from '../map/LiveRailwayMap';
import { TrackLegend } from '../map/TrackLegend';

interface LiveOperationsViewProps {
  state: SimulationState;
}

export const LiveOperationsView: React.FC<LiveOperationsViewProps> = ({ state }) => {
  return (
    <div className="space-y-4">
      <div className="bg-[#121826] border border-slate-800 rounded-xl p-3.5 flex justify-between items-center text-xs font-mono">
        <span className="text-slate-200 font-bold">TACTICAL LIVE OPERATIONS MAP — FULL SCREEN GIS RADAR</span>
        <span className="text-cyan-400">Sub-second telemetry refresh simulation</span>
      </div>

      <LiveRailwayMap
        workers={state.workers}
        trains={state.trains}
        workZones={state.workZones}
        blockSections={state.blockSections}
      />

      <TrackLegend />
    </div>
  );
};
