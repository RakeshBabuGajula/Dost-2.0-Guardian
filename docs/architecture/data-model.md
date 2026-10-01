# Conceptual Data Model & Database Schema: DOST Guardian 2.0

**Database System**: PostgreSQL 16 + PostGIS 3.4 Extension  

---

## 1. Entity-Relationship Diagram (ERD) Overview

```text
+-------------------+        +--------------------+        +---------------------+
|      users        | 1    * |   work_sessions    | *    1 |   block_sections    |
| (ID, Role, Name)  +--------+ (ID, Section, Status+--------+ (ID, Code, Geometry)|
+---------+---------+        +---------+----------+        +----------+----------+
          |                            |                              |
          | 1                          | 1                            | 1
          |                            |                              |
          | *                          | *                            | *
+---------v---------+        +---------v----------+        +----------v----------+
|  device_health    |        | worker_locations   |        |       trains        |
| (DeviceID, Batt)  |        | (WorkerID, Location|        | (TrainNo, Speed, Vector)
+-------------------+        +---------+----------+        +----------+----------+
                                       |                              |
                                       | 1                            | 1
                                       |                              |
                                       | *                            | *
                             +---------v----------+        +----------v----------+
                             |      alerts        |        |     near_misses     |
                             | (AlertID, State)   +--------+ (ID, MinDistance)    |
                             +--------------------+        +---------------------+
```

---

## 2. Core Relational Schemas

### 2.1 Table: `users`
- `id`: UUID (Primary Key, default `gen_random_uuid()`)
- `username`: VARCHAR(64) UNIQUE NOT NULL
- `password_hash`: VARCHAR(255) NOT NULL
- `full_name`: VARCHAR(128) NOT NULL
- `role`: VARCHAR(32) NOT NULL (`TRACK_WORKER`, `SUPERVISOR`, `SECTION_ENGINEER`, `CONTROL_ROOM`, `SAFETY_MANAGER`, `ADMIN`)
- `phone_number`: VARCHAR(20) NOT NULL
- `created_at`: TIMESTAMPTZ DEFAULT NOW()

### 2.2 Table: `block_sections`
- `id`: UUID (Primary Key)
- `code`: VARCHAR(32) UNIQUE NOT NULL (e.g., `MAS-AJJ-UP-120`)
- `name`: VARCHAR(128) NOT NULL
- `railway_division`: VARCHAR(64) NOT NULL
- `geometry`: GEOMETRY(LineString, 4326) NOT NULL (PostGIS spatial line representing track coordinates)
- `speed_limit_kmh`: INTEGER NOT NULL DEFAULT 110

### 2.3 Table: `work_sessions`
- `id`: UUID (Primary Key)
- `supervisor_id`: UUID REFERENCES `users(id)`
- `block_section_id`: UUID REFERENCES `block_sections(id)`
- `status`: VARCHAR(32) NOT NULL (`INITIATED`, `ACTIVE`, `CLOSING`, `CLOSED`)
- `start_time`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `end_time`: TIMESTAMPTZ NULL
- `work_zone_geometry`: GEOMETRY(Polygon, 4326) NOT NULL (Approved spatial polygon for gang work)

### 2.4 Table: `worker_locations` (Partitioned Hypertable / Spatial Telemetry)
- `id`: BIGSERIAL (Primary Key)
- `work_session_id`: UUID REFERENCES `work_sessions(id)`
- `worker_id`: UUID REFERENCES `users(id)`
- `recorded_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `location`: GEOMETRY(Point, 4326) NOT NULL
- `accuracy_meters`: FLOAT NOT NULL
- `heading_degrees`: FLOAT NULL
- `speed_mps`: FLOAT NULL
- `battery_level`: SMALLINT NOT NULL
- `network_state`: VARCHAR(16) NOT NULL (`ONLINE_4G`, `ONLINE_5G`, `BLE_MESH`, `OFFLINE`)

### 2.5 Table: `train_positions` (Live Vector Stream)
- `id`: BIGSERIAL (Primary Key)
- `train_number`: VARCHAR(32) NOT NULL (e.g., `EXP-12626`)
- `block_section_id`: UUID REFERENCES `block_sections(id)`
- `recorded_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `location`: GEOMETRY(Point, 4326) NOT NULL
- `speed_kmh`: FLOAT NOT NULL
- `direction_heading`: FLOAT NOT NULL
- `estimated_stopping_distance_m`: FLOAT NOT NULL

### 2.6 Table: `alerts`
- `id`: UUID (Primary Key)
- `work_session_id`: UUID REFERENCES `work_sessions(id)`
- `worker_id`: UUID REFERENCES `users(id)`
- `train_number`: VARCHAR(32) NOT NULL
- `state`: VARCHAR(32) NOT NULL (`CAUTION`, `WARNING`, `CRITICAL`, `EMERGENCY`)
- `time_to_danger_seconds`: INTEGER NOT NULL
- `created_at`: TIMESTAMPTZ DEFAULT NOW()
- `acknowledged_at`: TIMESTAMPTZ NULL
- `acknowledged_by`: UUID NULL REFERENCES `users(id)`
- `escalation_level`: SMALLINT DEFAULT 0 (`0=Worker`, `1=Supervisor`, `2=SectionEng`, `3=ControlRoom`)

### 2.7 Table: `near_misses`
- `id`: UUID (Primary Key)
- `work_session_id`: UUID REFERENCES `work_sessions(id)`
- `worker_id`: UUID REFERENCES `users(id)`
- `train_number`: VARCHAR(32) NOT NULL
- `occurred_at`: TIMESTAMPTZ DEFAULT NOW()
- `min_spatial_clearance_m`: FLOAT NOT NULL
- `ttd_at_ack_seconds`: INTEGER NOT NULL
- `location`: GEOMETRY(Point, 4326) NOT NULL
- `ai_summary`: TEXT NULL (Populated asynchronously by analytics service)

---

## 3. Spatial Indexing & Retention Strategy

1. **GiST Indexes**: Mandatory spatial indexes created on `geometry` and `location` columns:
   ```sql
   CREATE INDEX idx_worker_loc_spatial ON worker_locations USING GIST (location);
   CREATE INDEX idx_block_sec_spatial ON block_sections USING GIST (geometry);
   ```
2. **Table Partitioning**: `worker_locations` and `train_positions` partitioned monthly by `recorded_at` timestamp.
3. **Data Retention Policy**:
   - Live spatial locations compressed and aggregated after 30 days.
   - Core alert records, near-miss events, and audit logs retained permanently (7+ years).
