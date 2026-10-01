import { offlineDb, getPendingOfflineEvents, OfflineEventItem } from './offlineStore';
import { alertsApi } from '../../api/alerts';

export class OfflineSyncService {
  private isSyncing = false;
  private listeners: ((pendingCount: number) => void)[] = [];

  constructor() {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.synchronizePendingEvents();
      });
    }
  }

  public subscribeToBufferCount(listener: (pendingCount: number) => void): () => void {
    this.listeners.push(listener);
    this.notifyListeners();
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  private async notifyListeners() {
    try {
      const count = await offlineDb.events.where('status').equals('PENDING').count();
      this.listeners.forEach((l) => l(count));
    } catch {
      // Ignore in non-indexeddb environments
    }
  }

  public async synchronizePendingEvents(): Promise<void> {
    if (this.isSyncing) return;
    this.isSyncing = true;

    try {
      const pendingEvents = await getPendingOfflineEvents();
      for (const item of pendingEvents) {
        if (!item.id) continue;

        // Mark SYNCING
        await offlineDb.events.update(item.id, {
          status: 'SYNCING',
          attemptCount: item.attemptCount + 1,
          lastAttemptAt: new Date().toISOString(),
        });

        try {
          if (item.eventType === 'ALERT_ACKNOWLEDGED') {
            await alertsApi.acknowledgeAlert(
              item.payload.alertId as string,
              item.payload.workerId as string,
              item.payload.acknowledgedBy as string
            );
          } else if (item.eventType === 'EMERGENCY_TRIGGERED') {
            await alertsApi.triggerEmergency(
              item.payload.workerId as string,
              (item.payload.triggerType as string) || 'MANUAL_SOS'
            );
          }

          // Mark SYNCED
          await offlineDb.events.update(item.id, { status: 'SYNCED' });
        } catch {
          // If max attempts reached, mark FAILED, else revert to PENDING
          if (item.attemptCount >= 5) {
            await offlineDb.events.update(item.id, { status: 'FAILED' });
          } else {
            await offlineDb.events.update(item.id, { status: 'PENDING' });
          }
        }
      }
    } finally {
      this.isSyncing = false;
      await this.notifyListeners();
    }
  }
}

export const offlineSyncService = new OfflineSyncService();
