# Master Development Roadmap: DOST Guardian 2.0

---

## Engineering Phase Implementation Matrix

### Product Discovery
- **Objective**: Complete product discovery, research grounding, safety specifications, tech architecture, event models, UX guidelines, and project rules.
- **Deliverables**: Complete documentation set under `docs/`, `PROJECT_BRIEF.md`, `BLUEPRINT_SUMMARY.md`.
- **Dependencies**: None.
- **Acceptance Criteria**: Blueprint completed and internally consistency-checked; zero application code written; zero unverified DOST/Efftronics claims.

### Design System & Experience Foundation
- **Objective**: Implement centralized design tokens, Tailwind CSS theme, reusable component library, and interactive command center UI prototype shell.
- **Deliverables**: React web application foundation, application shell, command center dashboard, simulated live railway map, dynamic safety envelope visualization, and emergency alert UI.
- **Dependencies**: Product Discovery.
- **Acceptance Criteria**: High-contrast dark mode palette, WCAG AAA accessibility, 1-second alert layout visual verification, responsive layouts.

### Application Foundation (CURRENT DEVELOPMENT FOCUS)
- **Objective**: Build mobile and web app shell architectures, client state managers, REST/WebSocket connection managers, backend modular monolith foundation, and local storage layers.
- **Deliverables**: FastAPI backend monolith foundation, PostgreSQL + PostGIS schemas, Alembic migrations, Docker Compose setup, React state stores, API client interfaces, and IndexedDB offline buffer.
- **Dependencies**: Design System & Experience Foundation.
- **Acceptance Criteria**: Clean modular architecture, sub-50ms local state update targets, working backend REST & WebSocket interfaces.

### Data & Geospatial Platform
- **Objective**: Provision PostgreSQL + PostGIS database, create schemas, spatial indexes, spatial functions, and data retention policies.
- **Deliverables**: Database migrations, spatial index definitions, spatial query execution layer.
- **Dependencies**: Application Foundation.
- **Acceptance Criteria**: Spatial query performance targets under 10ms for active spatial queries.

### Railway Digital Twin
- **Objective**: Build standalone python railway simulator generating realistic train trajectories, speed profiles, and block occupations.
- **Deliverables**: `simulator/` engine, CLI control interface, Redis stream event producer.
- **Dependencies**: Data & Geospatial Platform.
- **Acceptance Criteria**: Simulates multiple trains and worker gangs simultaneously in real-time.

### Real-Time Safety Engine
- **Objective**: Implement pure deterministic `SafetyEngine` module calculating dynamic safety buffers, Time-to-Danger (TTD) countdowns, and state machine transitions.
- **Deliverables**: `SafetyEngine` Python module, state machine, vector projection math unit.
- **Dependencies**: Railway Digital Twin.
- **Acceptance Criteria**: Passes 15/15 automated safety scenario test suite.

### Worker Safety Platform
- **Objective**: Finalize worker mobile client experience, background GPS service, audio/haptic alert drivers, and offline degraded network mesh protocols.
- **Deliverables**: Mobile worker app production build, offline SQLite buffer manager, BLE peer mesh relay plugin.
- **Dependencies**: Real-Time Safety Engine.
- **Acceptance Criteria**: Full-screen siren override, offline countdown autonomy.

### Operations Command Center
- **Objective**: Build supervisor gang matrix, acknowledgment tracker, T1/T2/T3 multi-tier escalation timer loops, and live control room command deck.
- **Deliverables**: Supervisor tablet app, control room web dashboard, escalation manager.
- **Dependencies**: Worker Safety Platform.
- **Acceptance Criteria**: 100% of unacknowledged alerts trigger supervisor escalation at $T_1 = 10\text{s}$.

### Safety Intelligence
- **Objective**: Implement automated near-miss detection pipeline and spatial heatmap generation.
- **Deliverables**: Near-miss detector module, PostGIS spatial clustering queries, GIS heatmap visualization.
- **Dependencies**: Operations Command Center.
- **Acceptance Criteria**: Captures 100% of spatial clearance breaches $< 3.0\text{m}$.

### AI Analytics
- **Objective**: Build asynchronous AI analytics pipeline using pgvector and LLM RAG for post-shift safety insights.
- **Deliverables**: `ai/` module, report generator, pgvector search index.
- **Dependencies**: Safety Intelligence.
- **Acceptance Criteria**: Generates structured executive safety summaries from incident logs asynchronously without touching real-time safety critical path.

### Security & Validation
- **Objective**: Perform security audits, penetration testing, RBAC verification, and comprehensive end-to-end test execution.
- **Deliverables**: Automated test suites, security audit reports, compliance verification log.
- **Dependencies**: AI Analytics.
- **Acceptance Criteria**: Zero high/critical security vulnerabilities; 90%+ code coverage target.

### Deployment & Observability
- **Objective**: Finalize Docker production orchestration, Prometheus metrics, Grafana dashboards, and error monitoring.
- **Deliverables**: Docker compose prod spec, Grafana dashboard templates, Sentry error integration.
- **Dependencies**: Security & Validation.
- **Acceptance Criteria**: `[PROPOSED ENGINEERING TARGET]` 99.99% availability target; real-time latency monitoring dashboards.

### Authorized Integration Architecture
- **Objective**: Define secure abstract API adapters (`RailwayAdapter`) for future integration with real-world signaling systems (e.g., Data Loggers, Kavach/ETCS feeds).
- **Deliverables**: `RailwayAdapter` interface specs, hardware integration guidelines.
- **Dependencies**: Deployment & Observability.
- **Acceptance Criteria**: Isolated adapter layer preventing direct unvalidated access to core backend.
