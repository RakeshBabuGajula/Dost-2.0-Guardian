import React from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  Search,
  Bell,
  PanelLeftClose,
  PanelLeftOpen,
  Radio,
  Clock,
  Shield,
  Zap,
  Wifi,
  WifiOff,
  RefreshCw,
} from 'lucide-react';
import { SimulationScenarioId } from '../../types/simulation';
import { SIMULATION_SCENARIOS } from '../../simulation/scenarios';
import { OperationalDataMode, BackendConnectionState } from '../../types/backend';

interface TopBarProps {
  sidebarCollapsed: boolean;
  onToggleSidebar: () => void;
  isRunning: boolean;
  onToggleSimulation: () => void;
  onResetSimulation: () => void;
  speedMultiplier: number;
  onSetSpeed: (speed: number) => void;
  activeScenarioId: SimulationScenarioId;
  onSelectScenario: (scenarioId: SimulationScenarioId) => void;
  simulationTime: string;
  onOpenCommandPalette: () => void;
  unacknowledgedAlertCount: number;

  mode?: OperationalDataMode;
  connectionState?: BackendConnectionState;
  pendingOfflineEventCount?: number;
  onToggleMode?: (mode: OperationalDataMode) => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  sidebarCollapsed,
  onToggleSidebar,
  isRunning,
  onToggleSimulation,
  onResetSimulation,
  speedMultiplier,
  onSetSpeed,
  activeScenarioId,
  onSelectScenario,
  simulationTime,
  onOpenCommandPalette,
  unacknowledgedAlertCount,
  mode = 'simulation',
  connectionState = 'CONNECTED',
  pendingOfflineEventCount = 0,
  onToggleMode,
}) => {
  return (
    <header className="h-16 bg-[#0D1322] border-b border-slate-800 px-4 flex items-center justify-between z-10">
      {/* Left controls */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
          title="Toggle Navigation"
        >
          {sidebarCollapsed ? <PanelLeftOpen className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
        </button>

        {/* Search / Command Palette Trigger */}
        <button
          onClick={onOpenCommandPalette}
          className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 text-xs w-56 justify-between transition"
        >
          <div className="flex items-center space-x-2">
            <Search className="w-3.5 h-3.5 text-slate-400" />
            <span>Search or command...</span>
          </div>
          <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-slate-800 text-slate-400 rounded">Ctrl K</kbd>
        </button>
      </div>

      {/* Center Simulation Controls Panel */}
      <div className="hidden md:flex items-center space-x-3 bg-[#121826] px-3 py-1.5 rounded-xl border border-slate-800">
        <div className="flex items-center space-x-2">
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
            <Radio className="w-3 h-3 mr-1 animate-pulse" /> SIMULATOR
          </span>
          <select
            value={activeScenarioId}
            onChange={(e) => onSelectScenario(e.target.value as SimulationScenarioId)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2 py-1 focus:outline-none focus:border-cyan-500 max-w-[220px]"
          >
            {Object.values(SIMULATION_SCENARIOS).map((sc) => (
              <option key={sc.id} value={sc.id}>
                {sc.title}
              </option>
            ))}
          </select>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Play/Pause/Reset */}
        <div className="flex items-center space-x-1">
          <button
            onClick={onToggleSimulation}
            className={`p-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1 transition ${
              isRunning
                ? 'bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border border-amber-500/40'
                : 'bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30 border border-emerald-500/40'
            }`}
          >
            {isRunning ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span className="text-[11px] font-mono">{isRunning ? 'PAUSE' : 'START'}</span>
          </button>

          <button
            onClick={onResetSimulation}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            title="Reset Simulation"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Speed Toggles */}
        <div className="flex items-center space-x-1 text-[11px] font-mono">
          {[1, 2, 5].map((speed) => (
            <button
              key={speed}
              onClick={() => onSetSpeed(speed)}
              className={`px-1.5 py-0.5 rounded ${
                speedMultiplier === speed ? 'bg-cyan-500 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {speed}x
            </button>
          ))}
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Clock */}
        <div className="flex items-center space-x-1.5 text-xs font-mono text-cyan-400">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{simulationTime}</span>
        </div>
      </div>

      {/* Right User & Operational Connection Actions */}
      <div className="flex items-center space-x-3">
        {/* Connection & Mode Indicator Badge (Sections 19, 32, 46) */}
        <div className="flex items-center space-x-2">
          {mode === 'simulation' ? (
            <button
              onClick={() => onToggleMode && onToggleMode('backend')}
              className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-[11px] font-mono text-cyan-300 hover:bg-cyan-500/20 transition cursor-pointer"
              title="Click to switch to Backend Mode"
            >
              <Zap className="w-3 h-3 text-cyan-400" />
              <span>SIMULATION MODE</span>
            </button>
          ) : (
            <button
              onClick={() => onToggleMode && onToggleMode('simulation')}
              className={`hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-[11px] font-mono border transition cursor-pointer ${
                connectionState === 'CONNECTED'
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/20'
                  : connectionState === 'CONNECTING'
                  ? 'bg-amber-500/10 border-amber-500/30 text-amber-300 hover:bg-amber-500/20'
                  : 'bg-red-500/10 border-red-500/30 text-red-300 hover:bg-red-500/20'
              }`}
              title="Click to switch to Simulation Mode"
            >
              {connectionState === 'CONNECTED' ? (
                <>
                  <Wifi className="w-3 h-3 text-emerald-400" />
                  <span>BACKEND LIVE</span>
                </>
              ) : connectionState === 'CONNECTING' ? (
                <>
                  <RefreshCw className="w-3 h-3 text-amber-400 animate-spin" />
                  <span>CONNECTING</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3 text-red-400" />
                  <span>BACKEND OFFLINE</span>
                </>
              )}
            </button>
          )}

          {/* Offline Buffer Indicator */}
          {pendingOfflineEventCount > 0 && (
            <span
              className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30"
              title={`${pendingOfflineEventCount} offline event(s) buffered in IndexedDB`}
            >
              BUFFER: {pendingOfflineEventCount}
            </span>
          )}
        </div>

        {/* Notification Alert Bell */}
        <button
          onClick={onOpenCommandPalette}
          className="relative p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
        >
          <Bell className="w-5 h-5" />
          {unacknowledgedAlertCount > 0 && (
            <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full animate-ping" />
          )}
        </button>

        {/* User Profile */}
        <div className="flex items-center space-x-2.5 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-600 to-blue-700 flex items-center justify-center font-bold text-xs text-white shadow-sm">
            RK
          </div>
          <div className="hidden sm:flex flex-col">
            <span className="text-xs font-semibold text-slate-200 leading-tight">Rajesh Sharma</span>
            <span className="text-[10px] text-slate-400 font-mono">Section Supervisor</span>
          </div>
        </div>
      </div>
    </header>
  );
};
