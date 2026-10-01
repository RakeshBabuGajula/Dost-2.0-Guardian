import { OperationsDataProvider, OperationsState, BackendConnectionState } from '../../types/backend';
import { simulationEngine } from '../../simulation/simulationEngine';
import { SimulationState } from '../../types/simulation';

export class SimulationDataProvider implements OperationsDataProvider {
  private listeners: ((state: OperationsState) => void)[] = [];
  private unsubscribeEngine: (() => void) | null = null;

  constructor() {
    this.unsubscribeEngine = simulationEngine.subscribe(() => {
      this.notify();
    });
  }

  public getMode() {
    return 'simulation' as const;
  }

  public getConnectionState(): BackendConnectionState {
    return 'CONNECTED';
  }

  public getState(): OperationsState {
    const engineState: SimulationState = simulationEngine.getState();
    const activeCriticalAlert = engineState.activeCriticalAlert;

    return {
      mode: 'simulation',
      connectionState: 'CONNECTED',
      isRunning: engineState.isRunning,
      speedMultiplier: engineState.speedMultiplier,
      activeScenarioId: engineState.activeScenarioId,
      tickCount: engineState.tickCount,
      simulationTime: engineState.simulationTime,
      workers: engineState.workers,
      trains: engineState.trains,
      workZones: engineState.workZones,
      blockSections: engineState.blockSections,
      alerts: engineState.alerts,
      nearMisses: engineState.nearMisses,
      systemHealth: engineState.systemHealth,
      activeCriticalAlert,
      pendingOfflineEventCount: 0,
    };
  }

  public subscribe(listener: (state: OperationsState) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  private notify() {
    const currentState = this.getState();
    this.listeners.forEach((listener) => listener(currentState));
  }

  public start(): void {
    simulationEngine.start();
  }

  public pause(): void {
    simulationEngine.pause();
  }

  public reset(scenarioId?: string): void {
    simulationEngine.reset(scenarioId as any);
  }

  public setSpeedMultiplier(multiplier: number): void {
    simulationEngine.setSpeedMultiplier(multiplier);
  }

  public loadScenario(scenarioId: string): void {
    simulationEngine.loadScenario(scenarioId as any);
  }

  public async acknowledgeAlert(alertId: string, workerId: string): Promise<void> {
    simulationEngine.acknowledgeAlert(alertId, workerId);
  }

  public async triggerManualSos(workerId: string): Promise<void> {
    simulationEngine.triggerManualSos(workerId);
  }
}

export const simulationDataProvider = new SimulationDataProvider();
