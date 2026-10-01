import { OperationsDataProvider, OperationsState, BackendConnectionState } from '../../types/backend';
import { ReconnectingWebSocketClient } from '../realtime/websocketClient';
import { workersApi } from '../../api/workers';
import { trainsApi } from '../../api/trains';
import { alertsApi } from '../../api/alerts';
import { workZonesApi } from '../../api/workZones';
import { nearMissesApi } from '../../api/nearMisses';
import { storeOfflineEvent } from '../offline/offlineStore';
import { offlineSyncService } from '../offline/syncService';
import { Worker, Train, WorkZone, BlockSection } from '../../types/railway';
import { Alert, NearMissEvent } from '../../types/safety';

export class BackendDataProvider implements OperationsDataProvider {
  private wsClient: ReconnectingWebSocketClient;
  private connectionState: BackendConnectionState = 'OFFLINE';
  private listeners: ((state: OperationsState) => void)[] = [];

  private isRunning = true;
  private speedMultiplier = 1;
  private activeScenarioId = 'BACKEND_LIVE';
  private tickCount = 0;
  private simulationTime = new Date().toLocaleTimeString('en-US', { hour12: false });

  private workers: Worker[] = [];
  private trains: Train[] = [];
  private workZones: WorkZone[] = [];
  private blockSections: BlockSection[] = [];
  private alerts: Alert[] = [];
  private nearMisses: NearMissEvent[] = [];
  private systemHealth: any = [
    {
      component: 'PostgreSQL Spatial Engine',
      status: 'HEALTHY',
      latencyMs: 4,
      uptimePercentage: 99.99,
      lastCheckTime: 'Just now',
    },
    {
      component: 'WebSocket Real-Time Dispatcher',
      status: 'HEALTHY',
      latencyMs: 2,
      uptimePercentage: 99.98,
      lastCheckTime: 'Just now',
    },
  ];
  private pendingOfflineEventCount = 0;

  constructor() {
    this.wsClient = new ReconnectingWebSocketClient();

    this.wsClient.subscribeState((state) => {
      this.connectionState = state;
      if (state === 'CONNECTED') {
        this.fetchInitialRestData();
      }
      this.notify();
    });

    this.wsClient.subscribe((type, payload) => {
      this.handleWebSocketMessage(type, payload);
    });

    offlineSyncService.subscribeToBufferCount((count) => {
      this.pendingOfflineEventCount = count;
      this.notify();
    });

    // Start WebSocket connection
    this.wsClient.connect();
    this.fetchInitialRestData();
  }

  public getMode() {
    return 'backend' as const;
  }

  public getConnectionState(): BackendConnectionState {
    return this.connectionState;
  }

  public getState(): OperationsState {
    const activeCriticalAlert = this.alerts.find(
      (a) => !a.isAcknowledged && (a.state === 'CRITICAL' || a.state === 'EMERGENCY')
    );

    return {
      mode: 'backend',
      connectionState: this.connectionState,
      isRunning: this.isRunning,
      speedMultiplier: this.speedMultiplier,
      activeScenarioId: this.activeScenarioId,
      tickCount: this.tickCount,
      simulationTime: new Date().toLocaleTimeString('en-US', { hour12: false }),
      workers: this.workers,
      trains: this.trains,
      workZones: this.workZones,
      blockSections: this.blockSections,
      alerts: this.alerts,
      nearMisses: this.nearMisses,
      systemHealth: this.systemHealth,
      activeCriticalAlert,
      pendingOfflineEventCount: this.pendingOfflineEventCount,
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

  private async fetchInitialRestData() {
    try {
      const [workers, trains, alerts, workZones, nearMisses] = await Promise.allSettled([
        workersApi.getWorkers(),
        trainsApi.getTrains(),
        alertsApi.getAlerts(),
        workZonesApi.getWorkZones(),
        nearMissesApi.getNearMisses(),
      ]);

      if (workers.status === 'fulfilled') this.workers = workers.value;
      if (trains.status === 'fulfilled') this.trains = trains.value;
      if (alerts.status === 'fulfilled') this.alerts = alerts.value;
      if (workZones.status === 'fulfilled') this.workZones = workZones.value;
      if (nearMisses.status === 'fulfilled') this.nearMisses = nearMisses.value;

      this.connectionState = 'CONNECTED';
    } catch {
      this.connectionState = 'OFFLINE';
    }
    this.notify();
  }

  private handleWebSocketMessage(type: string, payload: any) {
    if (type === 'SNAPSHOT' && payload) {
      if (payload.workers) this.workers = payload.workers;
      if (payload.trains) this.trains = payload.trains;
      if (payload.alerts) this.alerts = payload.alerts;
    } else if (type === 'EVENT' && payload) {
      const eventType = payload.event_type;
      const data = payload.payload;

      if (eventType === 'ALERT_ACKNOWLEDGED' && data) {
        const alert = this.alerts.find((a) => a.id === data.id);
        if (alert) {
          alert.isAcknowledged = true;
          alert.state = 'SAFE';
        }
        const worker = this.workers.find((w) => w.id === data.workerId);
        if (worker) {
          worker.status = 'SAFE';
          worker.unacknowledgedAlertId = undefined;
        }
      } else if (eventType === 'EMERGENCY_TRIGGERED' && data) {
        const worker = this.workers.find((w) => w.id === data.worker_id);
        if (worker) {
          worker.status = 'EMERGENCY';
        }
      }
    }
    this.notify();
  }

  public start(): void {
    this.isRunning = true;
    this.notify();
  }

  public pause(): void {
    this.isRunning = false;
    this.notify();
  }

  public reset(scenarioId?: string): void {
    if (scenarioId) this.activeScenarioId = scenarioId;
    this.fetchInitialRestData();
  }

  public setSpeedMultiplier(multiplier: number): void {
    this.speedMultiplier = multiplier;
    this.notify();
  }

  public loadScenario(scenarioId: string): void {
    this.activeScenarioId = scenarioId;
    this.fetchInitialRestData();
  }

  public async acknowledgeAlert(alertId: string, workerId: string): Promise<void> {
    // Optimistic UI update
    const alert = this.alerts.find((a) => a.id === alertId);
    if (alert) {
      alert.isAcknowledged = true;
      alert.state = 'SAFE';
    }
    const worker = this.workers.find((w) => w.id === workerId);
    if (worker) {
      worker.status = 'SAFE';
      worker.unacknowledgedAlertId = undefined;
    }
    this.notify();

    if (this.connectionState === 'CONNECTED') {
      try {
        await alertsApi.acknowledgeAlert(alertId, workerId);
      } catch {
        // Fallback to offline store if network fails
        await storeOfflineEvent(`evt-ack-${alertId}`, 'ALERT_ACKNOWLEDGED', { alertId, workerId });
      }
    } else {
      // Offline mode: store in IndexedDB buffer
      await storeOfflineEvent(`evt-ack-${alertId}`, 'ALERT_ACKNOWLEDGED', { alertId, workerId });
    }
  }

  public async triggerManualSos(workerId: string): Promise<void> {
    const worker = this.workers.find((w) => w.id === workerId);
    if (worker) {
      worker.status = 'EMERGENCY';
    }
    this.notify();

    if (this.connectionState === 'CONNECTED') {
      try {
        await alertsApi.triggerEmergency(workerId, 'MANUAL_SOS');
      } catch {
        await storeOfflineEvent(`evt-sos-${workerId}`, 'EMERGENCY_TRIGGERED', { workerId, triggerType: 'MANUAL_SOS' });
      }
    } else {
      await storeOfflineEvent(`evt-sos-${workerId}`, 'EMERGENCY_TRIGGERED', { workerId, triggerType: 'MANUAL_SOS' });
    }
  }
}
