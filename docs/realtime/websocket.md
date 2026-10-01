# Real-Time WebSocket Architecture

## Endpoint
`ws://localhost:8000/api/v1/ws/operations`

## Synchronization Protocol (Snapshot + Delta)
1. **Connection**: Client establishes WebSocket connection.
2. **Snapshot Delivery**: Server immediately sends a complete `SNAPSHOT` payload containing current workers, trains, alerts, and system status.
3. **Event Streaming**: Server broadcasts lightweight `EVENT` deltas as state changes occur.

## Typed Message Schema
```json
{
  "type": "EVENT",
  "sequence": 42,
  "timestamp": "2026-09-30T16:30:00.000Z",
  "payload": {
    "event_id": "550e8400-e29b-41d4-a716-446655440000",
    "event_type": "TRAIN_POSITION_UPDATE",
    "schema_version": 1,
    "occurred_at": "2026-09-30T16:30:00.000Z",
    "source": "SIMULATOR",
    "correlation_id": "req-991823-abc",
    "entity_id": "TRN-204",
    "payload": {}
  }
}
```

## Reconnection Strategy
The frontend WebSocket client uses bounded exponential backoff with random jitter:
- Delays: 1s -> 2s -> 4s -> 8s -> 16s -> max 30s.
- Automatic `PING` / `PONG` heartbeat exchange every 15 seconds.
