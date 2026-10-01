# Spatial Architecture & Spatial Platform Specifications

**System**: DOST Guardian 2.0  
**Phase**: DATA & GEOSPATIAL PLATFORM  

---

## 1. Canonical Coordinate Reference System (CRS)

* **Primary CRS**: **WGS 84 (EPSG:4326)**
* **Representation**: All spatial coordinates are stored and transmitted in standard geographic WGS84 decimal degrees.
* **Coordinate Axis Order**: Explicit `(longitude, latitude)` in all WKT, GeoJSON, and PostGIS function calls (`ST_MakePoint(longitude, latitude)`).
* **Validation Bounds**:
  * Longitude: `[-180.0, 180.0]`
  * Latitude: `[-90.0, 90.0]`
  * Out-of-bounds coordinates trigger an HTTP `422 Unprocessable Entity` response.

---

## 2. Spatial Distance Strategy

* **Geodetic Measurement**: To avoid calculating planar degree distances, distance queries cast EPSG:4326 geometries to PostGIS `geography` types (`ST_DWithin(geom::geography, target::geography, radius_meters)`).
* **Distance Units**: All API response distances are returned in SI meters (`meters`).
* **Spatial Query Parameters**: All distance parameters (`radius_meters`) are documented strictly as **SPATIAL QUERY PARAMETERS**, not railway-certified safety thresholds.

---

## 3. PostGIS Spatial Indexing Strategy

GiST (Generalized Search Tree) spatial indexes are maintained on all primary geometry columns:

```sql
CREATE INDEX idx_workers_current_geom ON workers USING GIST (current_geom);
CREATE INDEX idx_trains_current_geom ON trains USING GIST (current_geom);
CREATE INDEX idx_work_zones_geom ON work_zones USING GIST (geom);
CREATE INDEX idx_block_sections_geom ON block_sections USING GIST (geom);
CREATE INDEX idx_safe_refuge_locations_geom ON safe_refuge_locations USING GIST (geom);
CREATE INDEX idx_track_segments_geom ON track_segments USING GIST (geom);
```

* **Query Optimization**: EXPLAIN ANALYZE verification confirms that point-in-polygon (`ST_Intersects`) and radius (`ST_DWithin`) queries perform index scans with execution times under < 1 ms.

---

## 4. Boundary & Temporal Semantics

1. **Polygon Boundary Semantics**: Points located on the boundary of a `WorkZone` or `SafetyZone` polygon are defined as **INSIDE** using `ST_Intersects`.
2. **Ambiguous Containment**: If a point falls between or inside multiple overlapping block section corridors, all matching candidate blocks are returned in `candidate_blocks` with `is_ambiguous = true`.
3. **Timezone Uniformity**: All spatial entity timestamps are parsed, stored, and returned in timezone-aware **UTC ISO-8601** format. Naive timestamps are strictly forbidden.

---

## 5. Non-Negotiable Safety Boundary Statement

The Data & Geospatial Platform provides factual spatial data operations only (such as proximity querying, containment checking, and distance calculations). It does **NOT** compute certified railway safety decisions, automatic track clearances, or evacuation authorizations.
