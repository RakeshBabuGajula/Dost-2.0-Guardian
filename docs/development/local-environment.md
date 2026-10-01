# Local Development Environment Guide

## Prerequisites
- Node.js 18+ & npm
- Python 3.11+
- Docker & Docker Compose

## Quick Start Commands

### 1. Frontend Development Server
```bash
npm install
npm run dev
```
App runs at `http://localhost:5173`.

### 2. Backend Server
```bash
python -m venv backend/venv
backend/venv/Scripts/pip install -r backend/requirements.txt
backend/venv/Scripts/uvicorn app.main:app --reload --port 8000
```
API runs at `http://localhost:8000`. OpenAPI docs at `http://localhost:8000/docs`.

### 3. Docker Compose Orchestration
```bash
docker compose up -d
```
Starts PostgreSQL + PostGIS (port 5432), Redis (port 6379), and Backend API container (port 8000).

### 4. Running Verification Tests
```bash
# Frontend simulation & integration test
npx tsc --noEmit
npx tsx src/tests/runTests.ts
npx tsx src/tests/integration.test.ts

# Backend pytest suite
pytest backend/tests/
```
