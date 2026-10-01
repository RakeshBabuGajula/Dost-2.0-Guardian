# Event Model Specification: DOST Guardian 2.0

**Event Transport**: Redis Streams & WebSockets (`wss://`)  
**Format**: JSON Standard Schema v1  


---

## 1. Real-Time Event Inventory

| Event Name | Producer | Primary Consumer | Idempotency Key Pattern | Target Delivery SLA `[PROPOSED ENGINEERING TARGET]` |
| :--- | :--- | :--- | :--- | :--- |
| `TRAIN_POSITION_UPDATE` | Simulator / Signal Feed | Safety Engine | `evt:train_pos:{train_id}:{timestamp_ms}` | $< 100\text{ ms}$ |
| `WORKER_LOCATION_UPDATE` | Worker Mobile App | Safety Engine, Supervisor Web | `evt:work_loc:{worker_id}:{timestamp_ms}` | $< 300\text{ ms}$ |
| `WORK_SESSION_STARTED` | Supervisor Mobile/Web | Backend Core, All Workers | `evt:sess_start:{session_id}` | $< 500\text{ ms}$ |
| `WORK_SESSION_ENDED` | Supervisor Mobile/Web | Backend Core, All Workers | `evt:sess_end:{session_id}` | $< 500\text{ ms}$ |
| `SAFETY_ZONE_CHANGED` | Safety Engine | Worker Mobile App | `evt:zone_chg:{worker_id}:{state}:{ts}` | $< 200\text{ ms}$ |
| `ALERT_CREATED` | Safety Engine | Worker App, Supervisor Web | `evt:alt_create:{alert_id}` | $< 150\text{ ms}$ |
| `ALERT_ESCALATED` | Safety Engine | Supervisor Web, Control Room | `evt:alt_esc:{alert_id}:{level}` | $< 200\text{ ms}$ |
| `ALERT_ACKNOWLEDGED` | Worker Mobile App | Safety Engine, Supervisor Web | `evt:alt_ack:{alert_id}` | $< 150\text{ ms}$ |
| `GPS_LOST` | Worker Mobile App | Safety Engine, Supervisor Web | `evt:gps_lost:{worker_id}:{ts}` | $< 500\text{ ms}$ |
| `NETWORK_LOST` | Gateway / Mobile App | Supervisor Web, BLE Mesh | `evt:net_lost:{worker_id}:{ts}` | $< 1000\text{ ms}$ |
| `BATTERY_LOW` | Worker Mobile App | Supervisor Web | `evt:batt_low:{worker_id}:{level}` | $< 2000\text{ ms}$ |
| `EMERGENCY_TRIGGERED` | Worker App / Control Room | Global Broadcast | `evt:emg_trig:{session_id}:{ts}` | $< 100\text{ ms}$ |
| `NEAR_MISS_DETECTED` | Safety Engine | Analytics Engine, Safety Manager| `evt:near_miss:{near_miss_id}` | Async |

---

## 2. Event Schema Definitions

### 2.1 `TRAIN_POSITION_UPDATE` Event Schema
```json
{
  "eventId": "evt_tp_883920194821",
  "eventName": "TRAIN_POSITION_UPDATE",
  "producer": "simulator.signalling_adapter",
  "timestamp": "2026-09-30T14:30:00.124Z",
  "payload": {
    "trainNumber": "EXP-12626",
    "blockSectionCode": "MAS-AJJ-UP-120",
    "coordinates": {
      "latitude": 13.0827,
      "longitude": 80.2707
    },
    "speedKmh": 110.5,
    "headingDegrees": 274.5,
    "estimatedStoppingDistanceMeters": 850.0
  }
}
```

### 2.2 `WORKER_LOCATION_UPDATE` Event Schema
```json
{
  "eventId": "evt_wl_994820192831",
  "eventName": "WORKER_LOCATION_UPDATE",
  "producer": "mobile.worker_app",
  "timestamp": "2026-09-30T14:30:00.312Z",
  "payload": {
    "workSessionId": "ws_77391-a8b2-491c",
    "workerId": "usr_worker_9921",
    "coordinates": {
      "latitude": 13.0831,
      "longitude": 80.2689
    },
    "accuracyMeters": 4.2,
    "speedMps": 0.8,
    "batteryLevel": 82,
    "networkState": "ONLINE_4G"
  }
}
```

### 2.3 `ALERT_CREATED` Event Schema
```json
{
  "eventId": "evt_ac_1029384756",
  "eventName": "ALERT_CREATED",
  "producer": "backend.safety_engine",
  "timestamp": "2026-09-30T14:30:00.450Z",
  "payload": {
    "alertId": "alt_8829104",
    "workSessionId": "ws_77391-a8b2-491c",
    "workerId": "usr_worker_9921",
    "trainNumber": "EXP-12626",
    "state": "CRITICAL",
    "timeToDangerSeconds": 75,
    "distanceToTrainMeters": 2100.0,
    "requiredAction": "MOVE_TO_DESIGNATED_SAFE_ZONE"
  }
}
```

---

## 3. Authoritative Event Idempotency & Deduplication Engine

To guarantee zero duplicate alert processing while handling high-throughput event streams:

1. **Authoritative Deterministic Store**:
   - Primary idempotency is enforced deterministically using **Redis `SET NX` key locks** (`idempotency:{event_id}`) with an explicit TTL (e.g., 300 seconds), combined with unique database primary key / `UNIQUE` constraints on event IDs in PostgreSQL.
   - If `SET NX` returns `0` (key already exists), the event is deterministically flagged as a duplicate and processed idempotently.

2. **Optional Bloom Filter Optimization**:
   - A Redis Bloom filter (`bf:events`) MAY be used as an optional preliminary pre-filtering optimization to quickly drop obvious duplicate IDs before querying the primary idempotency store.
   - A Bloom filter is strictly an optimization layer and is **NEVER** relied upon as the authoritative idempotency mechanism due to its non-zero false positive probability.

3. **Monotonic Telemetry Sequencing**:
   - Telemetry frames contain high-precision timestamps. Out-of-order stale telemetry frames ($t_{\text{frame}} < t_{\text{last\_processed}}$) are discarded.
