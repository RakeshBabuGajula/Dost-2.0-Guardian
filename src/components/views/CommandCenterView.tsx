import React, { useState } from 'react';
import { SimulationState } from '../../types/simulation';
import { MetricCard } from '../common/MetricCard';
import { StatusBadge } from '../common/StatusBadge';
import { LiveRailwayMap } from '../map/LiveRailwayMap';
import { SafetyEnvelopeView } from '../map/SafetyEnvelopeView';
import { TrackLegend } from '../map/TrackLegend';
import { AlertQueuePanel } from '../alerts/AlertQueuePanel';
import { AlertEscalationView } from '../alerts/AlertEscalationView';
import { AIAssistantDrawer } from '../ai/AIAssistantDrawer';
import { Users, MapPin, TrainTrack, BellRing, BatteryCharging, Signal, ShieldCheck, Bot, Filter, Clock, ChevronDown, ChevronUp } from 'lucide-react';

interface CommandCenterViewProps {
  state: SimulationState;
  onAcknowledgeAlert: (alertId: string, workerId: string) => void;
  onTriggerSos: (workerId: string) => void;
}

export const CommandCenterView: React.FC<CommandCenterViewProps> = ({
  state,
  onAcknowledgeAlert,
  onTriggerSos,
}) => {
  const [isAiDrawerOpen, setIsAiDrawerOpen] = useState(false);
  const [selectedSeverityFilter, setSelectedSeverityFilter] = useState<'ALL' | 'CRITICAL' | 'WARNING'>('ALL');
  const [selectedTelemetryFilter, setSelectedTelemetryFilter] = useState<'ALL' | 'DEGRADED' | 'LOW_BATTERY'>('ALL');
  const [isTimelineOpen, setIsTimelineOpen] = useState(true);

  // Filtered workers based on command center criteria
  const filteredWorkers = state.workers.filter((w) => {
    if (selectedSeverityFilter === 'CRITICAL' && w.status !== 'CRITICAL' && w.status !== 'EMERGENCY') return false;
    if (selectedSeverityFilter === 'WARNING' && w.status !== 'WARNING' && w.status !== 'CAUTION') return false;
    if (selectedTelemetryFilter === 'DEGRADED' && (w.networkState === 'ONLINE_4G' || w.networkState === 'ONLINE_5G')) return false;
    if (selectedTelemetryFilter === 'LOW_BATTERY' && w.batteryLevel >= 20) return false;
    return true;
  });

  const activeWorkersCount = state.workers.length;
  const activeWorkZonesCount = state.workZones.length;
  const trainsTrackedCount = state.trains.length;
  const criticalAlertsCount = state.alerts.filter((a) => !a.isAcknowledged && (a.state === 'CRITICAL' || a.state === 'EMERGENCY')).length;
  const lowBatteryCount = state.workers.filter((w) => w.batteryLevel < 20).length;
  const degradedNetworkCount = state.workers.filter((w) => w.networkState === 'OFFLINE' || w.networkState === 'BLE_MESH').length;
  const workersAtRisk = state.workers.filter((w) => w.status !== 'SAFE');

  const primaryWorker = state.workers[0];
  const primaryTrain = state.trains[0];

  return (
    <div className="space-y-6 relative">
      {/* AI Assistant Drawer Modal */}
      <AIAssistantDrawer isOpen={isAiDrawerOpen} onClose={() => setIsAiDrawerOpen(false)} />

      {/* Executive Operational Command Center Header Banner */}
      <div className="bg-[#121826] border border-cyan-500/30 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono tracking-wide">
              DOST GUARDIAN 2.0 — OPERATIONS COMMAND CENTER
            </h2>
            <p className="text-xs text-slate-400">
              Real-time worker safety, spatial intelligence & grounded AI analytics
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-[11px] font-mono">
          <button
            onClick={() => setIsAiDrawerOpen(true)}
            className="px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 text-cyan-300 rounded-xl flex items-center gap-2 font-bold transition-all shadow-md"
          >
            <Bot className="w-4 h-4 text-cyan-400" />
            DOST AI ASSISTANT
          </button>
          <span className="px-2.5 py-1.5 bg-slate-900 border border-slate-800 text-emerald-400 rounded-xl">
            [SIMULATION ACTIVE]
          </span>
        </div>
      </div>

      {/* TOP KPI GRID — Answering Key Operational Questions */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <MetricCard
          title="ACTIVE WORKERS"
          value={activeWorkersCount}
          subtitle={`${workersAtRisk.length} at elevated risk`}
          icon={<Users className="w-4 h-4 text-cyan-400" />}
          badgeColor="cyan"
        />
        <MetricCard
          title="ACTIVE WORK ZONES"
          value={activeWorkZonesCount}
          subtitle="Block MAS-AJJ-120/122"
          icon={<MapPin className="w-4 h-4 text-emerald-400" />}
          badgeColor="emerald"
        />
        <MetricCard
          title="TRAINS TRACKED"
          value={trainsTrackedCount}
          subtitle="Max speed 110 km/h"
          icon={<TrainTrack className="w-4 h-4 text-blue-400" />}
        />
        <MetricCard
          title="CRITICAL ALERTS"
          value={criticalAlertsCount}
          subtitle={criticalAlertsCount > 0 ? "REQUIRES IMMEDIATE ACTION" : "Zero unacknowledged"}
          icon={<BellRing className="w-4 h-4 text-red-400" />}
          badgeColor={criticalAlertsCount > 0 ? "red" : "default"}
        />
        <MetricCard
          title="LOW BATTERY (<20%)"
          value={lowBatteryCount}
          subtitle="Rajesh Sharma (14%)"
          icon={<BatteryCharging className="w-4 h-4 text-amber-400" />}
          badgeColor={lowBatteryCount > 0 ? "amber" : "default"}
        />
        <MetricCard
          title="DEGRADED MESH"
          value={degradedNetworkCount}
          subtitle={degradedNetworkCount > 0 ? "BLE Peer Mesh active" : "100% Cellular Online"}
          icon={<Signal className="w-4 h-4 text-orange-400" />}
          badgeColor={degradedNetworkCount > 0 ? "amber" : "default"}
        />
      </div>

      {/* OPERATIONAL FILTERS BAR */}
      <div className="bg-[#121826] border border-slate-800 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-cyan-400" />
          <span className="font-bold text-slate-200 uppercase">Operational Filters:</span>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center space-x-1.5">
            <span className="text-slate-400">Severity:</span>
            {(['ALL', 'CRITICAL', 'WARNING'] as const).map((sev) => (
              <button
                key={sev}
                onClick={() => setSelectedSeverityFilter(sev)}
                className={`px-2.5 py-1 rounded-lg border transition-all ${
                  selectedSeverityFilter === sev
                    ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300 font-bold'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                {sev}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-1.5">
            <span className="text-slate-400">Telemetry:</span>
            {(['ALL', 'DEGRADED', 'LOW_BATTERY'] as const).map((tel) => (
              <button
                key={tel}
                onClick={() => setSelectedTelemetryFilter(tel)}
                className={`px-2.5 py-1 rounded-lg border transition-all ${
                  selectedTelemetryFilter === tel
                    ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300 font-bold'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                {tel.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* MAIN TWO-COLUMN COMMAND CENTER LAYOUT */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Columns: Simulated GIS Map & Dynamic Safety Envelope */}
        <div className="lg:col-span-2 space-y-6">
          <LiveRailwayMap
            workers={filteredWorkers}
            trains={state.trains}
            workZones={state.workZones}
            blockSections={state.blockSections}
          />

          <TrackLegend />

          {/* Dynamic Safety Envelope Calculator Panel */}
          {primaryWorker && primaryTrain && (
            <SafetyEnvelopeView worker={primaryWorker} train={primaryTrain} />
          )}

          {/* Escalation Lifecycle View */}
          <AlertEscalationView alert={state.alerts[0]} />
        </div>

        {/* Right 1 Column: Live Alerts Queue & Worker Risk Roster */}
        <div className="space-y-6 flex flex-col justify-between">
          <AlertQueuePanel alerts={state.alerts} onAcknowledge={onAcknowledgeAlert} />

          {/* Worker Risk Roster Card */}
          <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-xs font-mono font-bold text-slate-100 uppercase tracking-wider">
                GANG SAFETY MATRIX ({filteredWorkers.length} SHOWN)
              </span>
              <span className="text-[10px] font-mono text-cyan-400">GANG 04</span>
            </div>

            <div className="space-y-2 max-h-64 overflow-y-auto">
              {filteredWorkers.map((worker) => (
                <div
                  key={worker.id}
                  className="p-2.5 bg-[#090D16] border border-slate-800 rounded-xl flex items-center justify-between"
                >
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-slate-200">{worker.name}</span>
                    <span className="text-[10px] font-mono text-slate-400">
                      Batt: {worker.batteryLevel}% | GPS: ±{worker.gpsAccuracyMeters}m
                    </span>
                  </div>
                  <StatusBadge status={worker.status} size="sm" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* OPERATIONAL EVENT TIMELINE DRAWER */}
      <div className="bg-[#121826] border border-slate-800 rounded-2xl p-4 space-y-3">
        <div
          onClick={() => setIsTimelineOpen(!isTimelineOpen)}
          className="flex items-center justify-between cursor-pointer select-none border-b border-slate-800 pb-2"
        >
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono font-bold text-slate-100 uppercase tracking-wider">
              LIVE OPERATIONAL CHRONOLOGICAL EVENT TIMELINE
            </span>
          </div>
          <button className="text-slate-400 hover:text-slate-200">
            {isTimelineOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>

        {isTimelineOpen && (
          <div className="space-y-2 max-h-48 overflow-y-auto font-mono text-xs">
            {state.alerts.map((a) => (
              <div key={a.id} className="p-2.5 bg-[#090D16] border border-slate-800 rounded-xl flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                    a.state === 'CRITICAL' || a.state === 'EMERGENCY' ? 'bg-red-500/20 text-red-300' : 'bg-amber-500/20 text-amber-300'
                  }`}>
                    {a.state}
                  </span>
                  <span className="text-slate-300">{a.id}: Train {a.trainId} approaching Worker {a.workerName} ({a.timeToDangerSeconds}s TTD)</span>
                </div>
                <span className="text-[10px] text-slate-400">{new Date(a.createdAt).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
