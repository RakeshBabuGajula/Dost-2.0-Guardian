# ADR 005: Canonical Spatial Reference Strategy and PostGIS Indexing Architecture

* **Context**: DOST Guardian 2.0 requires a queryable spatial railway domain to manage track topology, block sections, work zones, worker locations, train positions, and safe refuge niches.

---

## 1. Decision

1. **Canonical Coordinate Reference System**:
   We adopt **WGS 84 (EPSG:4326)** as the single authoritative coordinate reference system across all database entities, REST APIs, WebSocket events, and frontend map components.

2. **Geodetic Spatial Operations**:
   All distance-based spatial calculations use PostGIS `geography` type casting (`ST_DWithin` and `ST_Distance`) to ensure distance results reflect SI meters rather than planar degree approximations.

3. **GiST Indexing Architecture**:
   All high-frequency geometry columns (`workers.current_geom`, `trains.current_geom`, `work_zones.geom`, `block_sections.geom`, `safe_refuge_locations.geom`, `track_segments.geom`) are indexed using PostGIS **GiST (Generalized Search Tree)** indexes.

4. **Topology Graph Representation**:
   Railway topology is modeled as a directed spatial graph of `RailwayNode` elements connected by `TrackSegment` lines, supporting linear chainage referencing (`chainage_start_km` to `chainage_end_km`) and line directions (`UP`, `DOWN`, `BIDIRECTIONAL`).

5. **Non-Negotiable Safety Boundary**:
   The geospatial platform executes factual spatial operations only (e.g. proximity, containment, distance). It does not issue certified railway safety decisions or threshold authorizations.

---

## 2. Consequences

* **Positive**:
  * Unambiguous spatial coordinate exchange across backend REST/WebSocket and frontend SVG/GIS interfaces.
  * Sub-millisecond spatial query performance backed by GiST index scans (`0.224 ms` verified execution time for work zone point-in-polygon queries).
  * Extensible foundation for future Digital Twin and predictive safety engines.
* **Negative**:
  * Requires PostGIS extension to be enabled in PostgreSQL database.
