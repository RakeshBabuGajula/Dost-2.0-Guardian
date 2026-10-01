# Offline-First Browser Foundation & Synchronization

## Browser Local Store (Dexie.js IndexedDB)
When browser connectivity is lost (`navigator.onLine === false` or API calls fail), worker safety actions (e.g. Alert Acknowledgements, Emergency SOS triggers) are stored locally in IndexedDB.

### Database Schema (`DOST_Guardian_Offline_Store`)
- `events`: `++id`, `eventId`, `eventType`, `status`, `createdAt`, `payload`, `attemptCount`, `lastAttemptAt`.

## Synchronization Flow
```
User Action (Alert Ack / SOS)
             │
             ▼
      Network Check
      ┌──────┴──────┐
   [Online]     [Offline]
      │             │
      ▼             ▼
   Post API    Save IndexedDB (PENDING)
                    │
                    ▼
               Reconnected
                    │
                    ▼
          Sync Service Flush (SYNCING)
                    │
                    ▼
           Ack OK (SYNCED)
```
