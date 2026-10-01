# REST API Contracts Specification

All REST endpoints use the `/api/v1/` prefix and return strongly typed JSON payloads validated via Pydantic schemas.

## Endpoint Index

### Health & Diagnostics
- `GET /api/v1/health/live`: Liveness probe. Returns `{ "status": "UP" }`.
- `GET /api/v1/health/ready`: Readiness probe checking PostgreSQL and Redis.
- `GET /api/v1/health`: Diagnostic health status.

### Authentication Boundary
- `POST /api/v1/auth/login`: Authenticates synthetic development user and returns JWT token.
- `GET /api/v1/auth/me`: Retrieves current authenticated user profile and RBAC role.

### Workers Roster
- `GET /api/v1/workers`: List active gang maintainers and keymen.
- `GET /api/v1/workers/{worker_id}`: Retrieve worker detail and dynamic safety envelope parameters.
- `POST /api/v1/workers/{worker_id}/telemetry`: Ingest worker GPS and telemetry updates.

### Trains Telemetry
- `GET /api/v1/trains`: List active train positions and speeds.
- `GET /api/v1/trains/{train_id}`: Retrieve specific train telemetry.
- `POST /api/v1/trains/{train_id}/position`: Ingest train position updates.

### Alerts & Emergency Operations
- `GET /api/v1/alerts`: List safety alerts.
- `POST /api/v1/alerts/{alert_id}/acknowledge`: Acknowledge safety alert.
- `POST /api/v1/emergency-events`: Trigger manual SOS or emergency event (Idempotent).

### Work Zones & Near-Misses
- `GET /api/v1/work-zones`: Retrieve geofenced work zones.
- `GET /api/v1/near-misses`: Retrieve recorded near-miss incidents.
- `GET /api/v1/devices`: List handheld safety device telematics.
- `GET /api/v1/system/audit`: Retrieve operational audit trail logs.

## Standardized Error Format
```json
{
  "error": {
    "code": "WORKER_NOT_FOUND",
    "message": "Worker 'WRK-999' was not found",
    "request_id": "req-171293-abc",
    "details": {}
  }
}
```
