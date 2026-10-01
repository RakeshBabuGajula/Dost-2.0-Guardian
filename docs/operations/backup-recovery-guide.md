# DOST Guardian 2.0 — Operations & Recovery Guide
## PostgreSQL / PostGIS Backup, Point-In-Time Recovery & Observability Procedures

### 1. Database Backup Strategy

The DOST Guardian 2.0 platform uses PostgreSQL 16 with PostGIS 3.4 extensions. Database persistence is ensured via named Docker volume `postgres_data`.

#### Daily Automated Backup (Cron Command)
```bash
docker exec -t dost_postgres pg_dump -U postgres -d dost_guardian -F c -b -v -f /var/lib/postgresql/data/backups/dost_guardian_$(date +%Y%m%d_%H%M%S).dump
```

---

### 2. Database Restore Procedure

To restore from a binary `.dump` backup file:

```bash
# 1. Terminate active application connections
docker exec -t dost_postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'dost_guardian' AND pid <> pg_backend_pid();"

# 2. Drop and recreate database
docker exec -t dost_postgres psql -U postgres -c "DROP DATABASE IF EXISTS dost_guardian;"
docker exec -t dost_postgres psql -U postgres -c "CREATE DATABASE dost_guardian;"
docker exec -t dost_postgres psql -U postgres -d dost_guardian -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# 3. Restore schema & data
docker exec -t dost_postgres pg_restore -U postgres -d dost_guardian -v /var/lib/postgresql/data/backups/<backup_filename>.dump
```

---

### 3. Observability & Health Probes

| Health Probe | URL | Expected Response | Description |
|---|---|---|---|
| Liveness Probe | `GET /api/v1/health/live` | `{"status": "UP"}` | Verified FastAPI container liveness. |
| Readiness Probe | `GET /api/v1/health/ready` | `{"status": "HEALTHY", "db_connected": true}` | Verifies DB & Redis readiness. |
| Deep Diagnostic | `GET /api/v1/health/deep` | `{ "observability": { ... } }` | Detailed connection pool & telemetry counts. |
| Integration Contracts | `GET /api/v1/integration/contracts` | `{ "version": "v1.0-authorized-adapter" }` | External railway data contracts. |

---

### 4. Safety & Integration Isolation Policy

> [!CAUTION]
> **SAFETY BOUNDARY**: DOST Guardian 2.0 is **AUTHORIZED-INTEGRATION-READY** for development, demonstration, and simulation testing. It is **NOT** connected to live railway signalling or interlocking control. It does not claim SIL safety certification or live operational railway authority.
