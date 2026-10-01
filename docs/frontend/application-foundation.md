# Frontend Application Foundation

## Overview
The frontend of DOST Guardian 2.0 has been enhanced with a clean operational Data Provider abstraction pattern (`OperationsDataProvider`). This architecture enables smooth transition between local simulation mode and live backend server mode without altering the visual design system or existing UI view components.

## Data Provider Architecture
```
                         UI View Layer
                               │
                               ▼
                    OperationsDataProvider
                     (Abstract Interface)
                               │
               ┌───────────────┴───────────────┐
               │                               │
               ▼                               ▼
    SimulationDataProvider           BackendDataProvider
   (Deterministic Engine)            (REST API + WebSocket)
```

## State Architecture
1. **UI State**: `selectedWorker`, `selectedTrain`, `selectedAlert`, `activeView`, `sidebarCollapsed`, `isCommandPaletteOpen`.
2. **Operational State**: `workers`, `trains`, `workZones`, `alerts`, `nearMisses`, `systemHealth`.
3. **Connection State**: `CONNECTED`, `CONNECTING`, `DEGRADED`, `OFFLINE`.
4. **Simulation State**: `isRunning`, `speedMultiplier`, `activeScenarioId`, `tickCount`, `simulationTime`.

## Connection Status Badges
The header status badge dynamically reflects current operational modes:
- `SIMULATION MODE`: Running local deterministic simulation engine.
- `BACKEND LIVE`: Connected via WebSocket to backend FastAPI server.
- `BACKEND OFFLINE`: Backend server disconnected; offline event buffering active.
- `BUFFER: X`: Displayed when unsent worker events are buffered in browser IndexedDB.
