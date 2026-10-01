import Dexie, { type Table } from 'dexie';

export interface OfflineEventItem {
  id?: number;
  eventId: string;
  eventType: string;
  createdAt: string;
  payload: Record<string, unknown>;
  attemptCount: number;
  status: 'PENDING' | 'SYNCING' | 'SYNCED' | 'FAILED';
  lastAttemptAt?: string;
}

export class DostOfflineDatabase extends Dexie {
  events!: Table<OfflineEventItem>;

  constructor() {
    super('DOST_Guardian_Offline_Store');
    this.version(1).stores({
      events: '++id, eventId, eventType, status, createdAt',
    });
  }
}

export const offlineDb = new DostOfflineDatabase();

export const MAX_OFFLINE_BUFFER_ITEMS = 1000;

export async function storeOfflineEvent(
  eventId: string,
  eventType: string,
  payload: Record<string, unknown>
): Promise<OfflineEventItem> {
  const count = await offlineDb.events.count();
  if (count >= MAX_OFFLINE_BUFFER_ITEMS) {
    // Purge oldest synced or failed item to maintain bounded buffer (Section 20)
    const oldest = await offlineDb.events.orderBy('createdAt').first();
    if (oldest?.id) {
      await offlineDb.events.delete(oldest.id);
    }
  }

  const newItem: OfflineEventItem = {
    eventId,
    eventType,
    createdAt: new Date().toISOString(),
    payload,
    attemptCount: 0,
    status: 'PENDING',
  };

  const id = await offlineDb.events.add(newItem);
  return { ...newItem, id };
}

export async function getPendingOfflineEvents(): Promise<OfflineEventItem[]> {
  return offlineDb.events.where('status').equals('PENDING').toArray();
}

export async function getOfflineBufferCount(): Promise<number> {
  return offlineDb.events.where('status').equals('PENDING').count();
}
