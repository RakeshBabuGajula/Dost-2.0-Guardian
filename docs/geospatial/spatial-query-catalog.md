# PostGIS Spatial Query Catalog

**System**: DOST Guardian 2.0  
**Phase**: DATA & GEOSPATIAL PLATFORM  

---

## 1. Query Catalog

| Query Identifier | PostGIS Function | Primary Input | Target Entity | Index Strategy | Safety Critical? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `FIND_NEARBY_WORKERS` | `ST_DWithin(geom::geography, point::geography, radius)` | `lat, lng, radius_meters` | `Worker` | `GiST (workers.current_geom)` | NO (Informational) |
| `FIND_NEARBY_TRAINS` | `ST_DWithin(geom::geography, point::geography, radius)` | `lat, lng, radius_meters` | `Train` | `GiST (trains.current_geom)` | NO (Informational) |
| `WORKER_IN_WORK_ZONE` | `ST_Intersects(current_geom, work_zone.geom)` | `work_zone_id` | `Worker` | `GiST (work_zones.geom)` | NO (Informational) |
| `TRAIN_IN_WORK_ZONE` | `ST_Intersects(current_geom, work_zone.geom)` | `work_zone_id` | `Train` | `GiST (work_zones.geom)` | NO (Informational) |
| `CONTAINING_BLOCK` | `ST_Intersects(corridor_geom, point) / ST_DWithin` | `lat, lng` | `BlockSection` | `GiST (block_sections.corridor_geom)` | NO (Informational) |
| `NEARBY_TRACKS` | `ST_DWithin(geom::geography, point::geography, radius)` | `lat, lng, radius_meters` | `TrackSegment` | `GiST (track_segments.geom)` | NO (Informational) |
| `NEAREST_REFUGE_KNN` | `ST_Distance(geom::geography, point::geography)` | `lat, lng, limit` | `SafeRefugeLocation` | `GiST (safe_refuge_locations.geom)` | NO (Informational) |

---

## 2. Sample SQL Operations

### Nearby Workers Query
```sql
SELECT id, name, role, status,
       ST_Distance(current_geom::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) AS distance_meters
FROM workers
WHERE current_geom IS NOT NULL
  AND ST_DWithin(current_geom::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography, :radius_meters)
ORDER BY distance_meters ASC
LIMIT :limit OFFSET :offset;
```

### Work Zone Point Containment Query
```sql
SELECT w.id, w.name, w.role, w.status
FROM workers w
JOIN work_zones wz ON wz.id = :work_zone_id
WHERE w.current_geom IS NOT NULL
  AND ST_Intersects(w.current_geom, wz.geom)
LIMIT :limit OFFSET :offset;
```

### Nearest Safe Refuge KNN Query
```sql
SELECT r.id, r.code, r.name, r.refuge_type, r.capacity_persons,
       ST_Distance(r.geom::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) AS distance_meters
FROM safe_refuge_locations r
WHERE r.geom IS NOT NULL AND r.is_active = true
ORDER BY distance_meters ASC
LIMIT :limit;
```
