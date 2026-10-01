import { SimulationState, SimulationScenarioId } from '../types/simulation';
import {
  INITIAL_WORKERS,
  INITIAL_TRAINS,
  INITIAL_WORK_ZONES,
  INITIAL_BLOCK_SECTIONS,
  INITIAL_SYSTEM_HEALTH,
  INITIAL_NEAR_MISSES,
} from './mockData';
import { Alert, SafetyState } from '../types/safety';

export class DeterministicSimulationEngine {
  private state: SimulationState;
  private listeners: ((state: SimulationState) => void)[] = [];
  private timerId: number | null = null;

  constructor() {
    this.state = this.getInitialState('NORMAL_OPERATION');
  }

  public getInitialState(scenarioId: SimulationScenarioId = 'NORMAL_OPERATION'): SimulationState {
    const workers = JSON.parse(JSON.stringify(INITIAL_WORKERS));
    const trains = JSON.parse(JSON.stringify(INITIAL_TRAINS));
    const workZones = JSON.parse(JSON.stringify(INITIAL_WORK_ZONES));
    const blockSections = JSON.parse(JSON.stringify(INITIAL_BLOCK_SECTIONS));
    const systemHealth = JSON.parse(JSON.stringify(INITIAL_SYSTEM_HEALTH));
    const nearMisses = JSON.parse(JSON.stringify(INITIAL_NEAR_MISSES));

    return {
      isRunning: false,
      speedMultiplier: 1,
      activeScenarioId: scenarioId,
      tickCount: 0,
      simulationTime: new Date().toLocaleTimeString('en-US', { hour12: false }),
      workers,
      trains,
      workZones,
      blockSections,
      alerts: [],
      nearMisses,
      systemHealth,
      activeCriticalAlert: undefined,
    };
  }

  public getState(): SimulationState {
    return { ...this.state };
  }

  public subscribe(listener: (state: SimulationState) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  private notify() {
    const stateCopy = this.getState();
    this.listeners.forEach((listener) => listener(stateCopy));
  }

  public start() {
    if (this.state.isRunning) return;
    this.state.isRunning = true;
    this.scheduleNextTick();
    this.notify();
  }

  public pause() {
    this.state.isRunning = false;
    if (this.timerId !== null) {
      window.clearTimeout(this.timerId);
      this.timerId = null;
    }
    this.notify();
  }

  public reset(scenarioId?: SimulationScenarioId) {
    this.pause();
    const targetScenario = scenarioId || this.state.activeScenarioId;
    this.state = this.getInitialState(targetScenario);
    this.applyScenarioSetup(targetScenario);
    this.notify();
  }

  public setSpeedMultiplier(multiplier: number) {
    this.state.speedMultiplier = multiplier;
    this.notify();
  }

  public loadScenario(scenarioId: SimulationScenarioId) {
    this.pause();
    this.state = this.getInitialState(scenarioId);
    this.applyScenarioSetup(scenarioId);
    this.notify();
  }

  private applyScenarioSetup(scenarioId: SimulationScenarioId) {
    switch (scenarioId) {
      case 'TRAIN_APPROACHING':
        // Place train close to work zone (X=250 approaching X=450)
        this.state.trains[0].positionX = 250;
        this.state.trains[0].speedKmh = 110;
        break;

      case 'GPS_FAILURE':
        // Worker 101 GPS accuracy degrades to 42m
        this.state.workers[0].gpsAccuracyMeters = 42.0;
        this.state.workers[0].envelope.gpsUncertaintyBufferMeters = 42.0;
        this.state.workers[0].envelope.isExpandedDueToGps = true;
        this.state.workers[0].envelope.radiusMeters = 800; // expanded
        break;

      case 'NETWORK_FAILURE':
        // Worker 101 network drops
        this.state.workers[0].networkState = 'OFFLINE';
        this.state.workers[0].status = 'DEGRADED_NETWORK';
        break;

      case 'WORKER_UNACKNOWLEDGED':
        // Setup active critical alert for Ramesh unacknowledged
        this.state.trains[0].positionX = 350;
        this.createOrUpdateAlert('WRK-101', 'Ramesh Kumar', 'TRN-204', 'EXP-12626', 'MAS-AJJ-DOWN-120', 'EMERGENCY', 45, 1100, 'TIER_1_SUPERVISOR');
        break;

      case 'EMERGENCY_EVENT':
        // Worker Ramesh triggers SOS
        this.state.workers[0].status = 'EMERGENCY';
        this.createOrUpdateAlert('WRK-101', 'Ramesh Kumar', 'NONE', 'MANUAL SOS', 'MAS-AJJ-DOWN-120', 'EMERGENCY', 0, 0, 'TIER_3_CONTROL_ROOM');
        break;

      case 'NEAR_MISS':
        // Create near miss event record
        this.state.nearMisses.unshift({
          id: `NM-${Date.now().toString().slice(-4)}`,
          occurredAt: new Date().toISOString().replace('T', ' ').slice(0, 19),
          trainId: 'EXP-12626',
          trainSpeedKmh: 112,
          workerId: 'WRK-101',
          workerName: 'Ramesh Kumar',
          blockSectionCode: 'MAS-AJJ-DOWN-120',
          minSpatialClearanceMeters: 1.8,
          ttdAtAckSeconds: 12,
          severity: 'MODERATE',
          contributingFactors: ['Track Curve Blind Spot', 'Late Audio Notice (8s)', 'Wind Noise'],
          locationCoords: { x: 450, y: 140 },
        });
        break;

      case 'NORMAL_OPERATION':
      default:
        break;
    }
  }

  public acknowledgeAlert(alertId: string, workerId: string) {
    const alert = this.state.alerts.find((a) => a.id === alertId);
    if (alert) {
      alert.isAcknowledged = true;
      alert.acknowledgedAt = new Date().toISOString();
      alert.acknowledgedBy = 'Worker (Ramesh Kumar)';
      alert.state = 'SAFE';
    }

    const worker = this.state.workers.find((w) => w.id === workerId);
    if (worker) {
      worker.status = 'SAFE';
      worker.unacknowledgedAlertId = undefined;
    }

    if (this.state.activeCriticalAlert?.id === alertId) {
      this.state.activeCriticalAlert = undefined;
    }

    this.notify();
  }

  public triggerManualSos(workerId: string) {
    const worker = this.state.workers.find((w) => w.id === workerId);
    if (worker) {
      worker.status = 'EMERGENCY';
      this.createOrUpdateAlert(
        worker.id,
        worker.name,
        'MANUAL-SOS',
        'EMERGENCY BUTTON',
        worker.currentBlockSection,
        'EMERGENCY',
        0,
        0,
        'TIER_3_CONTROL_ROOM'
      );
    }
    this.notify();
  }

  private scheduleNextTick() {
    if (!this.state.isRunning) return;
    const intervalMs = Math.max(100, Math.floor(1000 / this.state.speedMultiplier));
    this.timerId = window.setTimeout(() => {
      this.tick();
      this.scheduleNextTick();
    }, intervalMs);
  }

  private tick() {
    this.state.tickCount += 1;
    this.state.simulationTime = new Date().toLocaleTimeString('en-US', { hour12: false });

    // 1. Move train EXP-12626 along Down Line (X=0 to X=1000)
    const train = this.state.trains[0];
    if (train) {
      const step = (train.speedKmh * 0.2) / 3.6; // step per tick
      train.positionX += step;
      if (train.positionX > 1000) {
        train.positionX = 0; // wrap around loop
      }
    }

    // 2. Evaluate TTD between Train 1 and Worker 101 (Ramesh)
    const worker1 = this.state.workers[0];
    if (train && worker1) {
      const distanceTrackUnits = worker1.position.x - train.positionX;
      // Convert track units to meters (1 unit = 10m)
      const distanceMeters = Math.max(0, distanceTrackUnits * 10);
      const trainSpeedMps = (train.speedKmh * 1000) / 3600;
      const ttdSeconds = trainSpeedMps > 0 ? Math.floor(distanceMeters / trainSpeedMps) : 999;

      if (distanceTrackUnits > 0 && distanceTrackUnits < 60) {
        // Train approaching worker within 600 meters
        let newState: SafetyState = 'SAFE';
        let requiredAction = 'MAINTAIN AWARENESS';

        if (ttdSeconds <= 90) {
          newState = 'CRITICAL';
          requiredAction = 'MOVE TO DESIGNATED SAFE REFUGE ZONE IMMEDIATELY';
        } else if (ttdSeconds <= 180) {
          newState = 'WARNING';
          requiredAction = 'PREPARE TO CLEAR TRACK';
        } else if (ttdSeconds <= 300) {
          newState = 'CAUTION';
          requiredAction = 'TRAIN IN ADJACENT SECTION';
        }

        if (worker1.status !== 'EMERGENCY' && !worker1.unacknowledgedAlertId) {
          worker1.status = newState;
          if (newState === 'CRITICAL' || newState === 'WARNING') {
            this.createOrUpdateAlert(
              worker1.id,
              worker1.name,
              train.number,
              train.name,
              worker1.currentBlockSection,
              newState,
              ttdSeconds,
              distanceMeters,
              ttdSeconds < 60 ? 'TIER_1_SUPERVISOR' : 'WORKER_ACK'
            );
          }
        }
      } else if (distanceTrackUnits <= 0 && distanceTrackUnits > -20) {
        // Train just passed worker
        if (worker1.status !== 'SAFE' && worker1.status !== 'DEGRADED_NETWORK') {
          worker1.status = 'SAFE';
          if (worker1.unacknowledgedAlertId) {
            const alert = this.state.alerts.find((a) => a.id === worker1.unacknowledgedAlertId);
            if (alert) {
              alert.isAcknowledged = true;
              alert.state = 'SAFE';
            }
            worker1.unacknowledgedAlertId = undefined;
          }
        }
      }
    }

    this.notify();
  }

  private createOrUpdateAlert(
    workerId: string,
    workerName: string,
    trainId: string,
    trainName: string,
    blockSectionCode: string,
    state: SafetyState,
    ttdSeconds: number,
    distanceMeters: number,
    escalationTier: Alert['escalationTier']
  ) {
    let alert = this.state.alerts.find((a) => a.workerId === workerId && !a.isAcknowledged);
    if (!alert) {
      alert = {
        id: `ALT-${Math.floor(1000 + Math.random() * 9000)}`,
        workerId,
        workerName,
        trainId,
        trainName,
        blockSectionCode,
        state,
        timeToDangerSeconds: ttdSeconds,
        distanceToTrainMeters: distanceMeters,
        escalationTier,
        createdAt: new Date().toLocaleTimeString('en-US', { hour12: false }),
        isAcknowledged: false,
        requiredAction: state === 'CRITICAL' ? 'MOVE TO DESIGNATED SAFE REFUGE ZONE IMMEDIATELY' : 'PREPARE TO CLEAR TRACK',
      };
      this.state.alerts.unshift(alert);
    } else {
      alert.state = state;
      alert.timeToDangerSeconds = ttdSeconds;
      alert.distanceToTrainMeters = distanceMeters;
      alert.escalationTier = escalationTier;
    }

    const worker = this.state.workers.find((w) => w.id === workerId);
    if (worker) {
      worker.unacknowledgedAlertId = alert.id;
    }

    if (state === 'CRITICAL' || state === 'EMERGENCY') {
      this.state.activeCriticalAlert = alert;
    }
  }
}

// Global simulation singleton instance
export const simulationEngine = new DeterministicSimulationEngine();
