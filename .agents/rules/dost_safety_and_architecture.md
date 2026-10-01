# DOST Guardian 2.0 Engineering & Architectural Rules

## 1. Grounding & Truthfulness
- **No Fake Railway Claims**: DOST Guardian 2.0 is an engineering prototype platform inspired by publicly documented railway worker safety principles. Do NOT present this prototype as an official Indian Railways system or railway-certified product.
- **No Unsupported DOST Feature Claims**: Clearly distinguish between facts verified from public DOST documentation (L2MRail / Indian Railways) and engineering inferences or proposed design features.
- **No Efftronics Attribution Error**: Do NOT claim Efftronics developed the public DOST app (developed by L2MRail). Efftronics specializes in signaling, data loggers, LC gate warnings, and digital block systems.
- **Strict Data Tagging**: All technical statements must use explicit classification tags: `[VERIFIED FACT]`, `[SOURCE-DERIVED INFORMATION]`, `[PROPOSED DESIGN]`, `[ENGINEERING INFERENCE]`, or `[PROPOSED ENGINEERING TARGET]`.

## 2. Safety-Critical Design Rules
- **AI Boundaries**: AI models (LLMs, neural nets, pattern classifiers) MUST NOT independently make or override safety-critical decisions. Safety-critical decisions must come strictly from deterministic, validated, and configurable safety rules.
- **Configurable Safety Thresholds**: Do NOT hard-code real railway safety thresholds or claim exact operational railway parameters without explicit configuration flags. All safety distances, warning times, and speed calculations must be marked as `CONFIGURABLE / SIMULATION VALUE`.
- **Fail-Safe Behavior**: In any failure mode (GPS loss, network disconnection, server timeout, battery low), the system must default to a conservative, safe state (e.g., degraded network safety alert, last-known-safe location tracking).

## 3. Architecture & Integration Rules
- **Idempotency**: Authoritative event idempotency must use deterministic mechanisms (e.g., unique event ID + database constraints, or Redis `SET NX` key locks). Bloom filters may only be used as optional preliminary pre-filtering optimizations.
- **Proposed Engineering Targets**: All latency, throughput, uptime, and performance metrics must be explicitly tagged as `[PROPOSED ENGINEERING TARGET]`.
- **Simulation Isolation**: Maintain a clear structural separation between the Railway Digital Twin (`simulator/` / mock simulation engine) and real-time backend/integration layers (`backend/`).
- **No Direct Live Railway Integration**: Real railway signaling interfaces must be accessed via abstract adapter interfaces (`RailwayAdapter`), never direct unvalidated calls to operational signaling networks.
- **Modular Monolith First**: Keep backend architecture clean, strongly typed, and structured as a modular monolith before considering microservices. Avoid unnecessary microservices or over-engineering.

## 4. Security & Compliance
- **Never Expose Secrets**: Zero hardcoded API keys, JWT secrets, or DB credentials in codebase or documentation. Use environment variables and configuration objects.
- **Role-Based Access Control (RBAC)**: Enforce strict permission boundaries across roles: Track Worker, Supervisor, Section Engineer, Control Room Operator, Safety Manager, System Admin.
- **Operational Data Sensitivity**: Treat worker real-time locations and train movement timelines as sensitive telemetry; encrypt in transit (TLS 1.3) and at rest (AES-256).

## 5. Professional Terminology
- **No Stage Numbering**: Public documentation, user interfaces, roadmaps, and comments must use professional engineering phase names (e.g., "Product Discovery", "Design System & Experience Foundation", "Real-Time Safety Engine", "Operations Command Center").
