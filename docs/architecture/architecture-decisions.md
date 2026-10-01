# Architecture Decision Records (ADRs): DOST Guardian 2.0

---

## ADR-01: Modular Monolith vs. Microservices Architecture

- **Status**: Approved
- **Context**: Real-time worker safety alerting requires sub-second event processing latency (< 300 ms). Introducing microservices at initial prototype development phases would add network serialization overhead, distributed tracing complexity, and deployment fragility.
- **Decision**: Adopt a **Modular Monolith** pattern using FastAPI (Python) structured by domain modules (`safety`, `sessions`, `telemetry`, `analytics`, `websocket`).
- **Consequences**:
  - *Positive*: Zero network hop latency between core modules; shared in-memory state during execution; simplified CI/CD and debugging.
  - *Negative*: Requires disciplined module boundary enforcement to prevent code tangling.

---

## ADR-02: Deterministic Safety Rule Engine vs. AI-Based Alerting

- **Status**: Approved
- **Context**: Machine learning models (e.g., neural networks or LLMs) are inherently non-deterministic and can hallucinate or fail silently under edge cases. Railway safety systems require verifiable safety compliance (CENELEC EN 50128).
- **Decision**: Implement a **100% Deterministic Safety Rule Engine** (`SafetyEngine`) using mathematical vector projections and explicit configurable rule matrices. AI is strictly restricted to offline analytics and near-miss reporting.
- **Consequences**:
  - *Positive*: 100% predictable, testable, and auditable safety behavior; zero risk of AI hallucination causing missed alerts.
  - *Negative*: Manual tuning required for complex multi-factor safety thresholds.

---

## ADR-03: Flutter for Worker Mobile Application

- **Status**: Approved
- **Context**: Track workers operate ruggedized smartphones requiring 60 fps smooth UI rendering, custom audio/vibration loops, background GPS/BLE service access, and cross-platform maintainability.
- **Decision**: Select **Flutter (Dart)** for the mobile application.
- **Consequences**:
  - *Positive*: Compiles directly to native ARM machine code; high visual performance; robust background task execution libraries.
  - *Negative*: Slightly larger APK binary size (~20 MB vs ~5 MB native Kotlin).

---

## ADR-04: Redis Streams for Real-Time Event Bus

- **Status**: Approved
- **Context**: The platform needs an event streaming bus to handle high-frequency train vector telemetry and worker location updates with low memory footprint and simple infrastructure setup.
- **Decision**: Utilize **Redis Streams** as the central event bus and in-memory spatial cache layer.
- **Consequences**:
  - *Positive*: Sub-millisecond pub/sub latency; low operational complexity; native integration with Redis cache.
  - *Negative*: Retains event history in memory; requires strict retention memory policy limits (`XADD MAXLEN`).
