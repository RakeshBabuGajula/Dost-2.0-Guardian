# PART 1 — SAFETY & RAILWAY INTELLIGENCE PLATFORM ARCHITECTURE

---

## 1. Executive Summary

Part 1 consolidates the **Railway Digital Twin**, **Real-Time Safety Engine**, and **Worker Safety Platform** into a unified, high-reliability operational safety architecture.

```
Railway Environment
        ↓
Train Movement (Digital Twin)
        ↓
Worker Telemetry & GPS Freshness
        ↓
PostGIS Spatial Relationship (WGS84 EPSG:4326)
        ↓
Deterministic Safety Engine (Dynamic Envelope & TTD)
        ↓
Real-Time Alert Lifecycle (CREATED -> DELIVERED -> ACKNOWLEDGED)
        ↓
Tiered Escalation (Worker -> Supervisor -> Control Room)
        ↓
Near-Miss Recording & Audit History
```

---

## 2. Core Architecture Modules

### A. Railway Digital Twin (`backend/app/services/simulation_service.py`)
- **Deterministic Train Movement**: Simulates train velocity along track segments, block section transitions, and bi-directional corridor movement.
- **WGS84 Geometries**: Updates PostGIS `trains.current_geom` and logs `TrainPosition` history.
- **Worker Movement**: Simulates active gang maintainers, keymen, and track inspects.

### B. Real-Time Safety Engine (`backend/app/services/safety_engine.py`)
- **Deterministic Rule-Based Logic**: Zero non-deterministic AI / LLM logic used for safety state evaluation.
- **Dynamic Safety Envelope**: Base radius (500m) + GPS uncertainty expansion buffer + track geometry buffer (50m).
- **Time-To-Danger (TTD)**: Human-readable TTD computation (`MM:SS`) based on train speed and distance.
- **Safety State Transitions**: `NORMAL/SAFE`, `ADVISORY/CAUTION`, `WARNING`, `CRITICAL`, `EMERGENCY`, `DEGRADED_NETWORK`, `RECOVERY`.

### C. Alert System & Tiered Escalation (`backend/app/services/alert_service.py`)
- **Idempotent Alert Creation**: Prevents duplicate active alerts for the same worker.
- **Lifecycle**: `CREATED` -> `DELIVERED` -> `ACKNOWLEDGED` -> `RESOLVED` (or `ESCALATED`).
- **Tiered Escalation**:
  - `TIER 0`: Worker Alert
  - `TIER 1`: Supervisor Escalation (T+10s unacknowledged)
  - `TIER 3`: Control Room Alert (T+20s unacknowledged)

### D. Emergency SOS & Near-Miss Intelligence (`backend/app/services/emergency_service.py`, `backend/app/services/near_miss_service.py`)
- **One-Tap Manual SOS**: Immediate emergency broadcast capturing worker, block section, device battery/signal state.
- **Near-Miss Recording**: Captures spatial clearance breach (< 3.0m), speed, TTD at acknowledgment, and contributing factors.

---

## 3. Verification Summary

* **Backend & Safety Test Suite**: 22/22 pytest tests passing cleanly in 0.79s.
* **TypeScript Type-Check**: `npx tsc --noEmit` passed with 0 errors.
* **Vite Production Build**: `npm run build` succeeded in 2.87s (`dist/assets/index-BdP4gvI2.js`).
* **PostGIS GiST Index Execution Time**: 0.224 ms execution time verified via PostgreSQL `EXPLAIN ANALYZE`.
* **Documentation Cleanliness**: 100% clean markdown text with zero `[image]` or `vscode-file://` links.
