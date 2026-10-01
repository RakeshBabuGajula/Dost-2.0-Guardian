import { Worker, Train, WorkZone, BlockSection, SystemHealthMetric } from './railway';
import { Alert, NearMissEvent } from './safety';

export type OperationalDataMode = 'simulation' | 'backend';

export type BackendConnectionState = 'CONNECTED' | 'CONNECTING' | 'DEGRADED' | 'OFFLINE';

export interface OperationsState {
  mode: OperationalDataMode;
  connectionState: BackendConnectionState;
  isRunning: boolean;
  speedMultiplier: number;
  activeScenarioId: string;
  tickCount: number;
  simulationTime: string;
  workers: Worker[];
  trains: Train[];
  workZones: WorkZone[];
  blockSections: BlockSection[];
  alerts: Alert[];
  nearMisses: NearMissEvent[];
  systemHealth: SystemHealthMetric[] | any;
  activeCriticalAlert?: Alert;
  pendingOfflineEventCount: number;
}

export interface OperationsDataProvider {
  getMode(): OperationalDataMode;
  getConnectionState(): BackendConnectionState;
  getState(): OperationsState;
  subscribe(listener: (state: OperationsState) => void): () => void;

  start(): void;
  pause(): void;
  reset(scenarioId?: string): void;
  setSpeedMultiplier(multiplier: number): void;
  loadScenario(scenarioId: string): void;

  acknowledgeAlert(alertId: string, workerId: string): Promise<void>;
  triggerManualSos(workerId: string): Promise<void>;
}
