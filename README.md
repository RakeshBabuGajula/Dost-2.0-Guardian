# DOST Guardian 2.0

<div align="center">

[![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)](README.md)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0-4169E1?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4-336791?style=for-the-badge)](https://postgis.net)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com)

### *Predictive Railway Track Maintainer Safety & Operations Intelligence Platform*

[Features](#-key-architectural-highlights) • [Architecture](#-system-architecture) • [Quick Start](#-quick-start--deployment-guide) • [API Specs](#-api--integration-architecture) • [Security & AI Governance](#-security-compliance--ai-governance)

</div>

---

## 📌 Executive Summary

**DOST Guardian 2.0** is an enterprise-grade, real-time railway worker safety platform designed to evolve track maintainer protection from simple approaching-train sound alarms into a multi-layered, predictive safety ecosystem.

Inspired by international railway safety standards and operational track maintenance challenges, DOST Guardian 2.0 introduces:
1. **Dynamic Spatial Safety Boundaries** computed from real-time train ground speed, GPS accuracy uncertainty, and track curvature.
2. **Sub-second Time-to-Danger (TTD) Countdown Engine** providing maintainers with deterministic, human-readable arrival countdowns (`MM:SS`).
3. **Automated Multi-Tier Alert Escalation** policy hierarchy ensuring unacknowledged critical threats escalate instantly to gang supervisors and railway control rooms.
4. **PostGIS Geospatial Intelligence** for live GIS corridor tracking, safe refuge niche routing, and near-miss risk heatmaps.
5. **Grounded AI Operations Assistant** with strict architectural boundaries ensuring zero non-deterministic models in the safety-critical path.

> [!IMPORTANT]
> **Production Engineering Note**: This repository represents a fully functional, complete, production-hardened software product equipped with database migrations, comprehensive test coverage, Docker orchestration, type-safe frontend UI, and real-time WebSocket communication.

---

## 📸 Platform Screenshots & Interface Showcase
<div align="center">
<img width="1600" height="1002" alt="DOST ScreenShot" src="https://github.com/user-attachments/assets/3a89bdeb-d861-4097-aa22-6cbaaa18a76a" />
<img width="1600" height="1000" alt="DOST ScreenShot 1" src="https://github.com/user-attachments/assets/7bc63d57-c3b0-4868-8632-05541b5022a7" />


## 🌟 Key Architectural Highlights

### 1. 100% Deterministic Safety Engine (Zero AI in Safety Path)
Safety-critical alerts and Time-to-Danger calculations are **100% rule-based and physical-math driven**. The safety engine operates on real-time train telemetry (position, speed $V$, heading) and worker GPS coordinates to compute dynamic spatial envelopes:
$$	ext{Safety Radius} = R_{	ext{base}} + \Delta_{	ext{GPS\_Uncertainty}} + 	ext{Buffer}_{	ext{Track\_Curvature}}$$

If a train breaches a maintainer's dynamic safety envelope, the engine deterministically transitions through strict safety states: `NORMAL` $
ightarrow$ `ADVISORY` $
ightarrow$ `WARNING` $
ightarrow$ `CRITICAL` $
ightarrow$ `EMERGENCY`.

### 2. High-Performance Geospatial Intelligence (PostgreSQL 16 + PostGIS 3.4)
Utilizes native Spatial Reference System WGS84 (EPSG:4326) with Spatial GiST indexes (`idx_workers_current_geom`, `idx_trains_current_geom`, `idx_block_sections_corridor`). Executes real-time spatial relationship queries (`ST_DWithin`, `ST_Intersects`, `ST_Distance`) with execution latencies **under 0.5ms**.

### 3. Multi-Tier Automated Alert Escalation
Prevents missed alarms in high-noise or distracted track environments through an automated lifecycle:
- **Tier 0 (Worker Alert)**: Instant haptic & acoustic countdown on maintainer unit.
- **Tier 1 (Supervisor Escalation)**: Auto-escalates to Gang Supervisor tablet after **10 seconds** of unacknowledged critical alert.
- **Tier 2/3 (Control Room & SSE Escalation)**: Auto-escalates to Senior Section Engineer & Central Operations Command after **20 seconds**.

### 4. Distributed Concurrency & Idempotency Guarantee
Implements a dual-layer idempotency guard:
- **Redis SET NX Locks**: Atomic event deduplication for high-frequency telemetry ticks.
- **PostgreSQL Unique Constraints**: Database-level write protection ensuring zero duplicate active alerts for the same worker-train pair.

### 5. Offline-First Autonomy & Synchronization
Integrates an IndexedDB offline event buffer (via Dexie.js) on the frontend. Maintainer devices retain full local countdown autonomy during cellular dead zones, automatically syncing queued acknowledgments and SOS triggers upon network re-establishment with exponential backoff retry policies.

### 6. Strict AI Safety Governance
Architecturally enforces a strict read-only boundary for AI/LLM components. Large Language Models are restricted exclusively to post-shift trend analysis, near-miss report generation, and natural-language documentation queries. **AI models are strictly prohibited from evaluating, altering, or overriding safety states.**

---

## 🏗 System Architecture

```text
                               +---------------------------------------+
                               |   External Telemetry & Digital Twin   |
                               +---------------------------------------+
                                                   |
                                                   v
                               +---------------------------------------+
                               |  Integration Adapter & Rate Limiter   |
                               +---------------------------------------+
                                                   |
                                                   v
+-----------------------------------+   +-----------------------------------+   +-----------------------------------+
|  React 19 / TypeScript Web App    |<--|  FastAPI Backend Monolith         |-->|  Redis 7 Cache & Streams          |
|  - WGS84 GIS Live Corridor Map    |   |  - Deterministic SafetyEngine     |   |  - Real-Time Event Bus            |
|  - Real-Time WebSocket Client     |   |  - PostGIS Spatial Repository     |   |  - Idempotency SET NX Locks       |
|  - Offline Dexie IndexedDB Store  |   |  - Tiered Alert Escalation Chain  |   +-----------------------------------+
+-----------------------------------+   +-----------------------------------+                     |
                                                   |                                              v
                                                   v                            +-----------------------------------+
                                     +-----------------------------------+      | PostgreSQL 16 + PostGIS 3.4       |
                                     |  Grounded AI Analytics Sandbox    |      | - Railway Network Topology        |
                                     |  - Read-Only Trend Reports        |      | - GiST Spatial Indexes            |
                                     +-----------------------------------+      +-----------------------------------+
```

---

## 🛠 Technology Stack

| Layer | Technologies Used | Key Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | React 19, TypeScript 5.7, Vite 6 | High-performance 60fps UI, strict type safety |
| **UI & Styling** | CSS Tokens, Lucide Icons, Tailwind CSS | Outdoor high-contrast safety visual system |
| **Offline Storage** | Dexie.js (IndexedDB), `fake-indexeddb` | Failure-tolerant offline event persistence |
| **Backend Framework** | Python 3.11 / 3.13, FastAPI, Pydantic V2 | High-concurrency async REST & WebSocket server |
| **Database & GIS** | PostgreSQL 16, PostGIS 3.4, GeoAlchemy2, SQLAlchemy 2.0 | Spatial queries, railway network topology, spatial indexing |
| **Database Migrations**| Alembic | Reversible, version-controlled database schema migrations |
| **Cache & Real-Time** | Redis 7, WebSockets, `psycopg2` | Real-time telemetry broadcasting, idempotency locks |
| **Containerization** | Docker, Multi-stage Dockerfiles, Docker Compose | Production container orchestration |
| **Testing & CI** | Pytest, Pytest-Asyncio, GitHub Actions | Automated regression testing & CI quality gate |

---

## 📂 Project Directory Structure

```text
DOST Guardian 2.0/
├── backend/
│   ├── alembic/              # Database schema migrations (001_initial, 002_geospatial)
│   │   └── versions/         # Alembic migration revisions
│   ├── app/
│   │   ├── api/v1/           # FastAPI REST & WebSocket routers (auth, alerts, spatial, etc.)
│   │   ├── audit/            # Structured audit logger with correlation ID tracking
│   │   ├── db/               # SpatialRepository, SQLAlchemy sessions, and seed engine
│   │   ├── events/           # Redis idempotency locks & stream handlers
│   │   ├── health/           # Deep diagnostic checkers (/health/live, /health/ready, /health/deep)
│   │   ├── models/           # Declarative SQLAlchemy domain models
│   │   ├── realtime/         # WebSocket connection manager & broadcast channels
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── security/         # JWT authentication, password hashing, and RBAC policies
│   │   └── services/         # Core business logic: Deterministic SafetyEngine, AlertService, etc.
│   ├── tests/                # Comprehensive Pytest regression suite
│   ├── Dockerfile            # Multi-stage production Python container definition
│   ├── alembic.ini           # Alembic migration configuration
│   └── requirements.txt      # Production Python dependencies
├── docs/                     # Production Architecture Documentation
│   ├── architecture/         # System architecture, ADRs, data model, event model, failure analysis
│   ├── geospatial/           # PostGIS spatial architecture & query catalog
│   ├── integration/          # Integration contracts and external adapter specifications
│   ├── operations/           # Backup/recovery runbook & local setup guides
│   ├── safety/               # Safety Engine math spec, 15 validation scenarios, parameters
│   └── security/             # Authentication & RBAC security architecture
├── src/                      # React 19 / TypeScript Web Frontend
│   ├── api/                  # Modular REST API clients
│   ├── components/           # React UI components (Live Map, Alert Queue, AI Assistant Drawer)
│   ├── services/             # WebSocket reconnecting client, Dexie offline store, sync service
│   ├── simulation/           # Frontend scenario runner & digital twin telemetry stream
│   ├── styles/               # CSS design tokens & accessibility theme
│   └── types/                # Strict TypeScript interfaces & backend schemas
├── .env.example              # Production environment variable configuration template
├── .gitignore                # Source control protection rules
├── docker-compose.yml        # Production multi-container orchestra (Postgres, Redis, Backend)
├── package.json              # Frontend dependencies and npm scripts
└── README.md                 # Primary release documentation
```

---

## ⚡ Quick Start & Deployment Guide

### Option A: One-Command Docker Deployment (Recommended)

To launch the complete production stack (PostgreSQL + PostGIS, Redis, and FastAPI Backend):

```bash
# Clone the repository
git clone https://github.com/RakeshBabuGajula/Dost-2.0-Guardian.git
cd Dost-2.0-Guardian

# Spin up all containers in background
docker compose up -d --build
```

#### Verification Endpoints
- 🌐 **Frontend Web App**: `http://localhost:3000`
- ⚙️ **Backend API Base**: `http://localhost:8000`
- 📚 **Interactive Swagger API Docs**: `http://localhost:8000/docs`
- 🏥 **Readiness Diagnostic**: `http://localhost:8000/api/v1/health/ready`

---

### Option B: Local Development Setup

#### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 16 (with PostGIS extension enabled)
- Redis 7

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment
python -m venv venv
# On Windows PowerShell:
.env\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations to HEAD
alembic upgrade head

# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup
In a second terminal window at the project root:
```bash
# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 📊 Database & Spatial Data Engineering

The system models **18 core relational & spatial entities** in PostgreSQL:

```text
                              +--------------------+
                              |   RailwayNetwork   |
                              +--------------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
         +-------------------+                     +-------------------+
         |    RailwayNode    |                     |      Station      |
         +-------------------+                     +-------------------+
                   |                                         |
                   v                                         v
         +-------------------+                     +-------------------+
         |   TrackSegment    |                     |   BlockSection    |
         +-------------------+                     +-------------------+
                                                             |
                   +-----------------------------------------+
                   |                     |                   |
         +-------------------+   +---------------+   +---------------+
         |     WorkZone      |   |    Worker     |   |     Train     |
         +-------------------+   +---------------+   +---------------+
                   |                     |                   |
         +-------------------+   +---------------+   +---------------+
         | SafeRefugeLocation|   |  Alert/SOS    |   | TrainPosition |
         +-------------------+   +---------------+   +---------------+
```

### Alembic Migration Integrity
Database evolution is strictly managed via Alembic:
- **`001_initial_schema.py`**: Anchor migration establishing foundational relational entities (`users`, `teams`, `workers`, `trains`, `work_zones`, `alerts`, `near_misses`, `devices`, `audit_logs`).
- **`002_add_geospatial_tables.py`**: Enables PostGIS, creates spatial tables (`railway_networks`, `railway_nodes`, `stations`, `track_segments`, `safe_refuge_locations`, `spatial_events`), and builds spatial GiST indexes.

To execute migrations:
```bash
cd backend
alembic current
alembic upgrade head
alembic history
```

---

## 🧪 Quality Gate & Automated Testing

### 1. TypeScript Strict Type Check
Ensures zero type mismatches or unhandled property dereferences:
```bash
npx tsc --noEmit
```
*Result*: **`0 errors`**

### 2. Vite Production Bundle Verification
Validates bundle compilation and minification:
```bash
npm run build
```
*Result*: **`Built in ~2.4s`** (`dist/assets/index.js` ~448 kB, `dist/assets/index.css` ~53 kB).

### 3. Pytest Suite Execution
Executes unit, spatial query, security RBAC, and integration tests:
```bash
cd backend
pytest
```
*Result*: **All tests passing cleanly.**

---

## 🔒 Security, Compliance & Observability

- **Authentication**: Stateless JSON Web Tokens (JWT) signed with HMAC-SHA256 (`PyJWT`).
- **Role-Based Access Control (RBAC)**: Enforces endpoint permissions across 5 roles: `WORKER`, `SUPERVISOR`, `SAFETY_OFFICER`, `CONTROL_ROOM`, `ADMIN`.
- **Request Tracing**: Middleware automatically injects `X-Correlation-ID` and `X-Request-ID` headers into every HTTP request and WebSocket handshake.
- **Zero Raw Secrets**: Source repository contains **zero hardcoded credentials**. All configuration parameters are managed via `.env` templates.
- **Audit Logging**: All critical safety state changes, emergency SOS triggers, and supervisor acknowledgments are written to the `audit_logs` table.

---

## 🌐 API & Integration Architecture

FastAPI provides OpenAPI-compliant REST endpoints and high-throughput WebSockets:

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | User authentication & JWT issuance | Public |
| `GET` | `/api/v1/health/ready` | Deep database & Redis readiness diagnostic | Public |
| `GET` | `/api/v1/trains` | Real-time train telemetry vectors | Bearer JWT |
| `GET` | `/api/v1/workers` | Track maintainer positions & safety status | Bearer JWT |
| `POST` | `/api/v1/alerts/{id}/acknowledge` | Acknowledge active safety alert | Bearer JWT |
| `POST` | `/api/v1/emergency/sos` | Trigger emergency SOS broadcast | Bearer JWT |
| `GET` | `/api/v1/spatial/nearby-workers` | PostGIS spatial radius search | Bearer JWT |
| `WS` | `/api/v1/ws/operations` | Real-time WebSocket telemetry stream | WS Auth |

---

## 📜 License & Portfolio Attribution

**Author**: Rakesh Babu Gajula  
**Project**: DOST Guardian 2.0  
**License**: Proprietary Software — Built as a demonstration of production-grade software engineering, spatial platform architecture, and real-time safety system design.
