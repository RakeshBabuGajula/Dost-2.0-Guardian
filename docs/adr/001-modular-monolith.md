# ADR-001: Modular Monolith Backend Architecture

## Status
Accepted

## Context
The DOST Guardian 2.0 application requires a structured backend platform to support REST APIs, real-time WebSocket telemetry distribution, and database persistence. Microservices, Kafka, or complex distributed topologies would introduce unnecessary operational overhead for this stage.

## Decision
Adopt a **Modular Monolith** pattern for the backend service using Python, FastAPI, and SQLAlchemy 2.x. Domain logic is separated into internal modules (`workers`, `trains`, `work_zones`, `alerts`, `devices`, `health`, `audit`, `events`) within a single deployable application container.

## Consequences
- **Positive**: Low operational complexity, single deployment target, simplified transactional boundary, high developer productivity.
- **Negative**: Requires discipline to enforce module boundaries internally.
