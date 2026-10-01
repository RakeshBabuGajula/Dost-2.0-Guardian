import { Worker, Train, WorkZone, BlockSection, SystemHealthMetric } from './railway';
import { Alert, NearMissEvent } from './safety';

export type SimulationScenarioId =
  | 'NORMAL_OPERATION'
  | 'TRAIN_APPROACHING'
  | 'MULTIPLE_WORKERS'
  | 'MULTIPLE_TRAINS'
  | 'GPS_FAILURE'
  | 'NETWORK_FAILURE'
  | 'WORKER_UNACKNOWLEDGED'
  | 'EMERGENCY_EVENT'
  | 'NEAR_MISS'
  | 'RECOVERY';

export interface SimulationScenario {
  id: SimulationScenarioId;
  title: string;
  description: string;
  initialStateSummary: string;
  triggerDescription: string;
}

export interface SimulationState {
  isRunning: boolean;
  speedMultiplier: number;
  activeScenarioId: SimulationScenarioId;
  tickCount: number;
  simulationTime: string;
  workers: Worker[];
  trains: Train[];
  workZones: WorkZone[];
  blockSections: BlockSection[];
  alerts: Alert[];
  nearMisses: NearMissEvent[];
  systemHealth: SystemHealthMetric[];
  activeCriticalAlert?: Alert;
}
