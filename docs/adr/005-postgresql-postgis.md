# ADR-005: PostgreSQL + PostGIS Spatial Database Foundation

## Status
Accepted

## Context
Future safety analytics and track section management require spatial calculations (geofencing, track clearance distances, spatial intersections).

## Decision
Use PostgreSQL 16 with PostGIS 3.4 spatial extensions and Alembic database migrations.

## Consequences
- **Positive**: Native spatial data types (`GEOMETRY`, `POLYGON`), spatial indexing (`GIST`), standardized spatial queries (`ST_DWithin`, `ST_Contains`).
- **Negative**: Requires PostGIS enabled PostgreSQL container image for local deployment.
