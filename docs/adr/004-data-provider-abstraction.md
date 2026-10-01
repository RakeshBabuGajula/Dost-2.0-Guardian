# ADR-004: Data Provider Abstraction for Simulation & Backend Modes

## Status
Accepted

## Context
The application must transition from frontend simulation mode to platform backend mode without breaking existing working React views or redesigning UI components.

## Decision
Introduce an `OperationsDataProvider` interface implemented by `SimulationDataProvider` and `BackendDataProvider`. The UI consumes this single interface.

## Consequences
- **Positive**: Complete UI isolation, seamless runtime provider switching (`VITE_DATA_MODE`), zero visual UI breakage.
- **Negative**: Requires maintaining interface parity across simulation and backend data structures.
