# DOST Guardian 2.0: Executive Project Brief

**Product Name**: DOST Guardian 2.0  
**Tagline**: *From Train Warning to Predictive Worker Safety*  
**Status**: **Blueprint Completed and Internally Consistency-Checked**  

---

## Executive Summary

**DOST Guardian 2.0** is an enterprise-grade, real-time railway worker safety platform designed to evolve track maintainer protection from simple approaching-train sound alerts into a multi-layered, predictive safety ecosystem.

Inspired by publicly documented railway safety initiatives (such as Indian Railways' DOST application developed by L2MRail) and international track safety standards, DOST Guardian 2.0 introduces dynamic spatial safety boundaries, deterministic time-to-danger countdowns, team accountability matrices, automated escalation chains, fail-safe offline autonomy, and post-shift near-miss intelligence.

> [!IMPORTANT]
> DOST Guardian 2.0 is an independent next-generation safety engineering prototype. It is NOT an official Indian Railways product, NOT a certified railway system, and NOT an Efftronics product.

---

## Core Differentiators & Next-Gen Capabilities

1. **Dynamic Safety Envelope**: Replaces static section alerts with dynamic spatial safety buffers computed from real-time train ground speed, track geometry, and worker location.
2. **Time-to-Danger (TTD) Engine**: Provides human-readable, sub-second urgency countdowns (e.g., `01:15 to arrival`) allowing field workers to digest threat severity within 1 second.
3. **Team Safety Accountability**: Enables gang supervisors to monitor real-time safe/warning/unacknowledged states across all team members on a field tablet dashboard.
4. **Multi-Tier Automated Escalation**: Escalates unacknowledged critical alerts up a strict policy hierarchy: Worker (T0) $\rightarrow$ Supervisor (T1: 10s) $\rightarrow$ Section Engineer & Control Room (T2/T3: 20s).
5. **Degraded Network Safety Mode**: Retains local countdown alerting and peer-to-peer BLE mesh heartbeats even during complete cellular network blackouts.
6. **Near-Miss Intelligence & Heatmaps**: Automatically logs spatial clearance breaches ($< 3.0\text{m}$) and generates risk heatmaps to identify recurring hazardous work zones.
7. **Strict AI Governance**: Enforces a strict separation of concerns where AI models are limited to offline trend analysis and report generation, while safety-critical decisions remain 100% deterministic.

---

## Architecture At A Glance

- **Worker Mobile App**: Flutter (Dart) — Native performance, 60 fps UI, outdoor high-contrast theme, background GPS/BLE service.
- **Supervisor & Control Room Web**: React + TypeScript + Tailwind CSS — Command center dashboard, Leaflet GIS live tracking.
- **Backend Monolith**: FastAPI (Python 3.12) — High-async performance, PostGIS spatial calculations, modular architecture.
- **Database & Cache**: PostgreSQL + PostGIS (spatial indexing) and Redis Streams (event bus) with Redis `SET NX` locks + DB constraints for authoritative idempotency.
- **Railway Digital Twin**: Isolated process generating realistic train vectors and block section telemetry for safe development and demonstration.

---

## Repository Structure Blueprint

```text
DOST 2.0/
├── .agents/rules/               # Project architectural & safety governance rules
├── docs/                        # Engineering Specifications & Specifications
│   ├── research/                # Fact-grounded landscape research (DOST vs Efftronics)
│   ├── product/                 # Vision, Personas, User Journeys, Feature Matrix, Requirements
│   ├── design/                  # Design System, UX Principles, Information Architecture
│   ├── architecture/            # System Architecture, Data Model, Event Model, Failure Analysis, ADRs
│   ├── safety/                  # Safety Engine, 15 Safety Scenarios, Configurable Assumptions
│   ├── ai/                      # AI Safety Boundaries & Governance
│   └── roadmap/                 # Master Engineering Phase Development Roadmap
├── PROJECT_BRIEF.md             # Executive Brief
└── BLUEPRINT_SUMMARY.md         # Blueprint Completion & Consistency-Check Summary
```
