import React, { useState, useEffect } from 'react';
import { Sidebar, NavView } from './Sidebar';
import { TopBar } from './TopBar';
import { CommandPalette } from './CommandPalette';
import { CriticalAlertOverlay } from '../alerts/CriticalAlertOverlay';
import { CommandCenterView } from '../views/CommandCenterView';
import { LiveOperationsView } from '../views/LiveOperationsView';
import { WorkerSafetyView } from '../views/WorkerSafetyView';
import { TeamSafetyView } from '../views/TeamSafetyView';
import { NearMissView } from '../views/NearMissView';
import { SafetyAnalyticsView } from '../views/SafetyAnalyticsView';
import { SystemHealthView } from '../views/SystemHealthView';
import { AuditEventsView } from '../views/AuditEventsView';
import { SettingsView } from '../views/SettingsView';

import { operationsManager } from '../../services/providers/operationsManager';
import { OperationsState, OperationalDataMode } from '../../types/backend';
import { SimulationScenarioId } from '../../types/simulation';

export const AppShell: React.FC = () => {
  const [provider, setProvider] = useState(() => operationsManager.getProvider());
  const [opsState, setOpsState] = useState<OperationsState>(() => provider.getState());
  const [currentView, setCurrentView] = useState<NavView>('command-center');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  useEffect(() => {
    const activeProv = operationsManager.getProvider();
    setProvider(activeProv);
    setOpsState(activeProv.getState());

    const unsubscribe = activeProv.subscribe((newState) => {
      setOpsState(newState);
    });

    return () => unsubscribe();
  }, [provider]);

  const handleToggleMode = (newMode: OperationalDataMode) => {
    operationsManager.setMode(newMode);
    const newProv = operationsManager.getProvider();
    setProvider(newProv);
    setOpsState(newProv.getState());
  };

  const unacknowledgedAlertCount = opsState.alerts.filter((a) => !a.isAcknowledged).length;

  const handleSelectScenario = (scenarioId: SimulationScenarioId) => {
    provider.loadScenario(scenarioId);
  };

  const handleAcknowledgeAlert = (alertId: string, workerId: string) => {
    provider.acknowledgeAlert(alertId, workerId);
  };

  const handleTriggerSos = (workerId: string) => {
    provider.triggerManualSos(workerId);
  };

  // Convert OperationsState to compatible view format for legacy view components
  const legacySimState: any = {
    isRunning: opsState.isRunning,
    speedMultiplier: opsState.speedMultiplier,
    activeScenarioId: opsState.activeScenarioId,
    tickCount: opsState.tickCount,
    simulationTime: opsState.simulationTime,
    workers: opsState.workers,
    trains: opsState.trains,
    workZones: opsState.workZones,
    blockSections: opsState.blockSections,
    alerts: opsState.alerts,
    nearMisses: opsState.nearMisses,
    systemHealth: opsState.systemHealth,
    activeCriticalAlert: opsState.activeCriticalAlert,
  };

  return (
    <div className="flex h-screen w-screen bg-[#090D16] text-slate-100 overflow-hidden font-sans">
      {/* Left Collapsible Sidebar */}
      <Sidebar
        currentView={currentView}
        onSelectView={setCurrentView}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        unacknowledgedAlertCount={unacknowledgedAlertCount}
      />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Operational Header */}
        <TopBar
          sidebarCollapsed={sidebarCollapsed}
          onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          isRunning={opsState.isRunning}
          onToggleSimulation={() => (opsState.isRunning ? provider.pause() : provider.start())}
          onResetSimulation={() => provider.reset()}
          speedMultiplier={opsState.speedMultiplier}
          onSetSpeed={(speed) => provider.setSpeedMultiplier(speed)}
          activeScenarioId={opsState.activeScenarioId as SimulationScenarioId}
          onSelectScenario={handleSelectScenario}
          simulationTime={opsState.simulationTime}
          onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
          unacknowledgedAlertCount={unacknowledgedAlertCount}
          mode={opsState.mode}
          connectionState={opsState.connectionState}
          pendingOfflineEventCount={opsState.pendingOfflineEventCount}
          onToggleMode={handleToggleMode}
        />

        {/* Dynamic Route View Renderer */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 bg-[#090D16]">
          {currentView === 'command-center' && (
            <CommandCenterView
              state={legacySimState}
              onAcknowledgeAlert={handleAcknowledgeAlert}
              onTriggerSos={handleTriggerSos}
            />
          )}
          {currentView === 'live-ops' && <LiveOperationsView state={legacySimState} />}
          {currentView === 'worker-safety' && (
            <WorkerSafetyView
              state={legacySimState}
              onAcknowledgeAlert={handleAcknowledgeAlert}
              onTriggerSos={handleTriggerSos}
            />
          )}
          {currentView === 'team-safety' && (
            <TeamSafetyView state={legacySimState} onAcknowledgeAlert={handleAcknowledgeAlert} />
          )}
          {currentView === 'work-zones' && <LiveOperationsView state={legacySimState} />}
          {currentView === 'trains' && <LiveOperationsView state={legacySimState} />}
          {currentView === 'alerts' && (
            <CommandCenterView
              state={legacySimState}
              onAcknowledgeAlert={handleAcknowledgeAlert}
              onTriggerSos={handleTriggerSos}
            />
          )}
          {currentView === 'near-misses' && <NearMissView state={legacySimState} />}
          {currentView === 'analytics' && <SafetyAnalyticsView state={legacySimState} />}
          {currentView === 'system-health' && <SystemHealthView state={legacySimState} />}
          {currentView === 'audit-events' && <AuditEventsView state={legacySimState} />}
          {currentView === 'settings' && <SettingsView />}
        </main>
      </div>

      {/* Command Palette Modal (Ctrl+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSelectView={setCurrentView}
        onSelectScenario={handleSelectScenario}
      />

      {/* Full-Screen 1-Second Emergency Alert Overlay */}
      {opsState.activeCriticalAlert && !opsState.activeCriticalAlert.isAcknowledged && (
        <CriticalAlertOverlay
          alert={opsState.activeCriticalAlert}
          onAcknowledge={handleAcknowledgeAlert}
          onTriggerSos={handleTriggerSos}
        />
      )}
    </div>
  );
};
