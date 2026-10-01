# Authentication & Role-Based Access Control (RBAC)

## Roles Specification
1. **WORKER**: View own safety envelope, acknowledge own alerts, trigger manual SOS.
2. **SUPERVISOR**: View assigned team roster, monitor team alerts, acknowledge/escalate alerts.
3. **CONTROL_ROOM**: Monitor system-wide operational state, view escalations, manage emergency events.
4. **ADMIN**: User administration and operational configuration.
5. **AUDITOR**: Read-only access to immutable audit log trails.

## Token Boundary
Development authentication issues JWT tokens containing `sub`, `username`, `role`, and expiration claims. Tokens are transmitted in the standard HTTP `Authorization: Bearer <token>` header.
