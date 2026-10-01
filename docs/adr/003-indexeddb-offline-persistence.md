# ADR-003: IndexedDB / Dexie.js for Browser Offline Persistence

## Status
Accepted

## Context
Worker handheld devices and web clients may experience transient network drops in remote railway corridors. Safety-critical actions performed offline must be preserved and synchronized upon network restoration.

## Decision
Use `Dexie.js` as an IndexedDB wrapper in the browser to maintain a bounded offline event buffer (`DOST_Guardian_Offline_Store`).

## Consequences
- **Positive**: Reliable browser local persistence, non-blocking asynchronous storage, clean synchronization lifecycle (`PENDING` -> `SYNCING` -> `SYNCED`).
- **Negative**: Browser storage limits require explicit buffer bounds (capped at 1,000 items).
