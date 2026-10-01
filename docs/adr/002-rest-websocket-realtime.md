# ADR-002: REST + WebSocket Real-Time Event Architecture

## Status
Accepted

## Context
High-frequency train telemetry and worker position updates require immediate distribution to connected browser clients, while standard data fetching requires structured REST semantics.

## Decision
Combine REST API v1 (`/api/v1/`) endpoints for request-response operations with a WebSocket channel (`/api/v1/ws/operations`) utilizing a **Snapshot + Delta** synchronization protocol.

## Consequences
- **Positive**: Low latency event delivery, initial state recovery via snapshot on connect, fallback REST endpoints.
- **Negative**: Client must handle WebSocket disconnection and exponential backoff reconnection.
