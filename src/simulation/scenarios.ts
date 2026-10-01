import { SimulationScenario, SimulationScenarioId } from '../types/simulation';

export const SIMULATION_SCENARIOS: Record<SimulationScenarioId, SimulationScenario> = {
  NORMAL_OPERATION: {
    id: 'NORMAL_OPERATION',
    title: '1. Normal Railway Operation',
    description: 'All trains operating at standard speed on clear sections; workers active in assigned work zones in SAFE state.',
    initialStateSummary: 'Train EXP-12626 at Km 118, Gang 04 active at Km 120.',
    triggerDescription: 'Baseline steady-state operation.',
  },
  TRAIN_APPROACHING: {
    id: 'TRAIN_APPROACHING',
    title: '2. Train Approaching Active Work Zone',
    description: 'Express train EXP-12626 advances into Block Section MAS-AJJ-DOWN-120 heading towards active gang.',
    initialStateSummary: 'Train moves from X=50 towards X=450 at 110 km/h.',
    triggerDescription: 'Triggers CAUTION -> WARNING -> CRITICAL state transitions and TTD countdown.',
  },
  MULTIPLE_WORKERS: {
    id: 'MULTIPLE_WORKERS',
    title: '3. Multi-Worker Gang Coordination',
    description: 'Gang 04 members spread across 100 meters of track receive coordinated alert telemetry.',
    initialStateSummary: 'Workers Ramesh, Suresh, Rajesh monitored simultaneously.',
    triggerDescription: 'Demonstrates gang status matrix and multi-worker state synchronization.',
  },
  MULTIPLE_TRAINS: {
    id: 'MULTIPLE_TRAINS',
    title: '4. Bi-Directional Multi-Train Traffic',
    description: 'Two trains (EXP-12626 Down Line & SF-12601 Up Line) approach adjacent sections simultaneously.',
    initialStateSummary: 'Trains moving from opposing directions towards work zone.',
    triggerDescription: 'Evaluates priority resolution for closest threat vector.',
  },
  GPS_FAILURE: {
    id: 'GPS_FAILURE',
    title: '5. GNSS GPS Lock Degradation',
    description: 'Worker Ramesh enters rock cutting section; GPS accuracy degrades from 4.2m to 42m.',
    initialStateSummary: 'GPS accuracy drops to 42m.',
    triggerDescription: 'Triggers Dynamic Safety Envelope expansion (+200m) and spatial uncertainty ring.',
  },
  NETWORK_FAILURE: {
    id: 'NETWORK_FAILURE',
    title: '6. Cellular Network Disconnection',
    description: 'Worker Ramesh loses 4G connectivity in deep cutting; 0 bars signal.',
    initialStateSummary: 'WebSocket heartbeat times out.',
    triggerDescription: 'App transitions to Degraded Network Safety Mode; local countdown & BLE mesh active.',
  },
  WORKER_UNACKNOWLEDGED: {
    id: 'WORKER_UNACKNOWLEDGED',
    title: '7. Unacknowledged Alert & Tiered Escalation',
    description: 'Worker receives CRITICAL alert but fails to tap I\'M SAFE within 10 seconds.',
    initialStateSummary: 'CRITICAL alert unacknowledged at T+10s.',
    triggerDescription: 'Triggers Tier-1 Supervisor Escalation and Tier-2 Control Room Alert.',
  },
  EMERGENCY_EVENT: {
    id: 'EMERGENCY_EVENT',
    title: '8. Manual Worker SOS Emergency Trigger',
    description: 'Worker Ramesh encounters track hazard/injury and presses manual emergency SOS button.',
    initialStateSummary: 'Worker triggers manual SOS.',
    triggerDescription: 'Instant emergency broadcast to Supervisor tablet and Control Room.',
  },
  NEAR_MISS: {
    id: 'NEAR_MISS',
    title: '9. Spatial Near-Miss Spatial Clearance Breach',
    description: 'Train passes worker location with only 1.8m spatial clearance (below 3.0m clearance threshold).',
    initialStateSummary: 'Spatial clearance measured at 1.8m.',
    triggerDescription: 'Logs near-miss incident card and updates Safety Heatmap.',
  },
  RECOVERY: {
    id: 'RECOVERY',
    title: '10. Alert Resolution & Section Clear',
    description: 'Train passes clear of work section; worker acknowledges safety; system reverts to SAFE.',
    initialStateSummary: 'Train exits section.',
    triggerDescription: 'Reverts state machine to SAFE baseline.',
  },
};
