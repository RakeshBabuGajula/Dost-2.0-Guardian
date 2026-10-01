"""Add PostGIS geospatial tables, geometry columns, and GiST indexes with idempotent SQL

Revision ID: 002_add_geospatial_tables
Revises: 001_initial_schema


"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '002_add_geospatial_tables'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. Add columns to existing tables safely
    op.execute("ALTER TABLE block_sections ADD COLUMN IF NOT EXISTS network_id VARCHAR(36);")
    op.execute("ALTER TABLE block_sections ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'ACTIVE';")
    op.execute("ALTER TABLE block_sections ADD COLUMN IF NOT EXISTS geom geometry(LINESTRING, 4326);")
    op.execute("ALTER TABLE block_sections ADD COLUMN IF NOT EXISTS corridor_geom geometry(POLYGON, 4326);")

    op.execute("ALTER TABLE work_zones ADD COLUMN IF NOT EXISTS description TEXT;")
    op.execute("ALTER TABLE work_zones ADD COLUMN IF NOT EXISTS block_section_id VARCHAR(36);")
    op.execute("ALTER TABLE work_zones ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'ACTIVE';")
    op.execute("ALTER TABLE work_zones ADD COLUMN IF NOT EXISTS geom geometry(POLYGON, 4326);")

    op.execute("ALTER TABLE safety_zones ADD COLUMN IF NOT EXISTS geom geometry(POLYGON, 4326);")

    op.execute("ALTER TABLE workers ADD COLUMN IF NOT EXISTS current_geom geometry(POINT, 4326);")
    op.execute("ALTER TABLE workers ADD COLUMN IF NOT EXISTS last_location_at TIMESTAMP WITH TIME ZONE;")

    op.execute("ALTER TABLE worker_locations ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'SIMULATOR';")
    op.execute("ALTER TABLE worker_locations ADD COLUMN IF NOT EXISTS device_id VARCHAR(50);")
    op.execute("ALTER TABLE worker_locations ADD COLUMN IF NOT EXISTS sequence INTEGER DEFAULT 1;")
    op.execute("ALTER TABLE worker_locations ADD COLUMN IF NOT EXISTS geom geometry(POINT, 4326);")

    op.execute("ALTER TABLE trains ADD COLUMN IF NOT EXISTS heading DOUBLE PRECISION DEFAULT 90.0;")
    op.execute("ALTER TABLE trains ADD COLUMN IF NOT EXISTS current_geom geometry(POINT, 4326);")
    op.execute("ALTER TABLE trains ADD COLUMN IF NOT EXISTS last_position_at TIMESTAMP WITH TIME ZONE;")

    op.execute("ALTER TABLE train_positions ADD COLUMN IF NOT EXISTS heading DOUBLE PRECISION DEFAULT 90.0;")
    op.execute("ALTER TABLE train_positions ADD COLUMN IF NOT EXISTS direction VARCHAR(20) DEFAULT 'EASTBOUND';")
    op.execute("ALTER TABLE train_positions ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'SIMULATOR';")
    op.execute("ALTER TABLE train_positions ADD COLUMN IF NOT EXISTS sequence INTEGER DEFAULT 1;")
    op.execute("ALTER TABLE train_positions ADD COLUMN IF NOT EXISTS geom geometry(POINT, 4326);")

    op.execute("ALTER TABLE devices ADD COLUMN IF NOT EXISTS current_geom geometry(POINT, 4326);")
    op.execute("ALTER TABLE near_misses ADD COLUMN IF NOT EXISTS geom geometry(POINT, 4326);")

    # 3. Create new spatial tables if not exists
    op.execute("""
    CREATE TABLE IF NOT EXISTS railway_networks (
        id VARCHAR(36) PRIMARY KEY,
        code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        srid INTEGER NOT NULL DEFAULT 4326,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS railway_nodes (
        id VARCHAR(36) PRIMARY KEY,
        network_id VARCHAR(36) REFERENCES railway_networks(id),
        code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        node_type VARCHAR(50) NOT NULL,
        position_x DOUBLE PRECISION NOT NULL,
        position_y DOUBLE PRECISION NOT NULL,
        geom geometry(POINT, 4326),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id VARCHAR(36) PRIMARY KEY,
        network_id VARCHAR(36) REFERENCES railway_networks(id),
        code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        station_type VARCHAR(50) NOT NULL,
        position_x DOUBLE PRECISION NOT NULL,
        position_y DOUBLE PRECISION NOT NULL,
        geom geometry(POINT, 4326),
        boundary_geom geometry(POLYGON, 4326),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS track_segments (
        id VARCHAR(36) PRIMARY KEY,
        network_id VARCHAR(36) REFERENCES railway_networks(id),
        code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        start_node_id VARCHAR(36) REFERENCES railway_nodes(id),
        end_node_id VARCHAR(36) REFERENCES railway_nodes(id),
        track_code VARCHAR(50) NOT NULL,
        direction VARCHAR(20) NOT NULL,
        chainage_start_km DOUBLE PRECISION NOT NULL,
        chainage_end_km DOUBLE PRECISION NOT NULL,
        length_meters DOUBLE PRECISION NOT NULL,
        speed_limit_kmh INTEGER NOT NULL,
        block_section_id VARCHAR(36) REFERENCES block_sections(id),
        status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
        geom geometry(LINESTRING, 4326),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS safe_refuge_locations (
        id VARCHAR(36) PRIMARY KEY,
        work_zone_id VARCHAR(50) REFERENCES work_zones(id),
        code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        refuge_type VARCHAR(50) DEFAULT 'NICHE' NOT NULL,
        capacity_persons INTEGER DEFAULT 10 NOT NULL,
        position_x DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
        position_y DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
        geom geometry(POINT, 4326),
        boundary_geom geometry(POLYGON, 4326),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS device_locations (
        id VARCHAR(36) PRIMARY KEY,
        device_id VARCHAR(50) REFERENCES devices(id),
        worker_id VARCHAR(50) REFERENCES workers(id),
        position_x DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
        position_y DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
        gps_accuracy_meters DOUBLE PRECISION DEFAULT 2.5 NOT NULL,
        battery_percentage INTEGER DEFAULT 95 NOT NULL,
        network_signal_dbm INTEGER DEFAULT -72 NOT NULL,
        source VARCHAR(50) DEFAULT 'HARDWARE_UNIT' NOT NULL,
        sequence INTEGER DEFAULT 1 NOT NULL,
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
        geom geometry(POINT, 4326)
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS spatial_events (
        id VARCHAR(36) PRIMARY KEY,
        event_type VARCHAR(100) NOT NULL,
        entity_type VARCHAR(50) NOT NULL,
        entity_id VARCHAR(50) NOT NULL,
        target_type VARCHAR(50),
        target_id VARCHAR(50),
        distance_meters DOUBLE PRECISION,
        details JSON,
        geom geometry(GEOMETRY, 4326),
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """)

    # 4. GiST Indexes
    op.execute("CREATE INDEX IF NOT EXISTS idx_railway_nodes_geom ON railway_nodes USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_stations_geom ON stations USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_track_segments_geom ON track_segments USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_block_sections_geom ON block_sections USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_block_sections_corridor ON block_sections USING GIST (corridor_geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_work_zones_geom ON work_zones USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_safety_zones_geom ON safety_zones USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_safe_refuge_locations_geom ON safe_refuge_locations USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_workers_current_geom ON workers USING GIST (current_geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_worker_locations_geom ON worker_locations USING GIST (geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_trains_current_geom ON trains USING GIST (current_geom);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_train_positions_geom ON train_positions USING GIST (geom);")


def downgrade() -> None:
    pass
