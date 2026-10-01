# Backend Application Foundation

## Overview
The backend for DOST Guardian 2.0 is built as a high-performance **Modular Monolith** using Python, FastAPI, Uvicorn, Pydantic v2, and SQLAlchemy 2.x. It delivers REST API endpoints, real-time WebSocket event distribution, PostGIS geospatial data persistence, and idempotent event processing.

## Modular Monolith Structure
The backend is structured into domain modules located within `backend/app/`:
- `auth`: Development authentication boundary and JWT token handling.
- `workers`: Roster management, status tracking, dynamic envelope properties.
- `trains`: Locomotive positioning and speed telemetry.
- `work_zones`: Geofenced track segments and safety buffers.
- `alerts`: Safety alerts and escalation tier state transitions.
- `near_misses`: Clearance breach events and contributing factors.
- `devices`: Handheld safety unit health and telemetry.
- `health`: Liveness and readiness diagnostic probes.
- `events`: Idempotency coordinator with Redis fast lock and DB constraints.
- `audit`: Immutable operational audit logging.

## Database & Alembic Migrations
- **Database Engine**: PostgreSQL 16 with PostGIS 3.4 extensions enabled.
- **Migrations**: Alembic version control (`backend/alembic/versions/`).
- **Seed Data**: Deterministic synthetic operational records populated on startup (`backend/app/db/init_db.py`).
