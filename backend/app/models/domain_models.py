import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="WORKER")  # WORKER, SUPERVISOR, CONTROL_ROOM, ADMIN, AUDITOR
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    worker = relationship("Worker", back_populates="user", uselist=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    supervisor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_section = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    workers = relationship("Worker", back_populates="team")


class RailwayNetwork(Base):
    __tablename__ = "railway_networks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False, index=True)  # MAS-AJJ-NET
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    srid = Column(Integer, nullable=False, default=4326)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    nodes = relationship("RailwayNode", back_populates="network")
    tracks = relationship("TrackSegment", back_populates="network")
    stations = relationship("Station", back_populates="network")
    blocks = relationship("BlockSection", back_populates="network")


class RailwayNode(Base):
    __tablename__ = "railway_nodes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    network_id = Column(String(36), ForeignKey("railway_networks.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # NODE-MAS-01
    name = Column(String(255), nullable=False)
    node_type = Column(String(50), nullable=False, default="JUNCTION")  # JUNCTION, SWITCH, SIGNAL, TERMINUS, CROSSING
    position_x = Column(Float, nullable=False, default=0.0)
    position_y = Column(Float, nullable=False, default=0.0)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    network = relationship("RailwayNetwork", back_populates="nodes")


class TrackSegment(Base):
    __tablename__ = "track_segments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    network_id = Column(String(36), ForeignKey("railway_networks.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # TS-MAS-AJJ-D1
    name = Column(String(255), nullable=False)
    start_node_id = Column(String(36), ForeignKey("railway_nodes.id"), nullable=False)
    end_node_id = Column(String(36), ForeignKey("railway_nodes.id"), nullable=False)
    track_code = Column(String(50), nullable=False, index=True)  # DOWN_MAIN, UP_MAIN
    direction = Column(String(20), nullable=False, default="DOWN")  # UP, DOWN, BIDIRECTIONAL
    chainage_start_km = Column(Float, nullable=False, default=0.0)
    chainage_end_km = Column(Float, nullable=False, default=5.0)
    length_meters = Column(Float, nullable=False, default=5000.0)
    speed_limit_kmh = Column(Integer, nullable=False, default=110)
    block_section_id = Column(String(36), ForeignKey("block_sections.id"), nullable=True)
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE, MAINTENANCE, SUSPENDED
    geom = Column(Geometry("LINESTRING", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    network = relationship("RailwayNetwork", back_populates="tracks")
    block_section = relationship("BlockSection", back_populates="track_segments")


class Station(Base):
    __tablename__ = "stations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    network_id = Column(String(36), ForeignKey("railway_networks.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # MAS, AJJ
    name = Column(String(255), nullable=False)
    station_type = Column(String(50), nullable=False, default="PASSENGER")  # PASSENGER, JUNCTION, FREIGHT
    position_x = Column(Float, nullable=False, default=0.0)
    position_y = Column(Float, nullable=False, default=0.0)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)
    boundary_geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    network = relationship("RailwayNetwork", back_populates="stations")


class BlockSection(Base):
    __tablename__ = "block_sections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    network_id = Column(String(36), ForeignKey("railway_networks.id"), nullable=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)  # MAS-AJJ-DOWN-120
    name = Column(String(255), nullable=False)
    line_type = Column(String(50), nullable=False, default="DOWN")  # UP, DOWN, BIDIRECTIONAL
    start_km = Column(Float, nullable=False)
    end_km = Column(Float, nullable=False)
    speed_limit_kmh = Column(Integer, nullable=False, default=110)
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, MAINTENANCE, UNKNOWN
    is_active = Column(Boolean, default=True)
    geom = Column(Geometry("LINESTRING", srid=4326), nullable=True)
    corridor_geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    network = relationship("RailwayNetwork", back_populates="blocks")
    track_segments = relationship("TrackSegment", back_populates="block_section")
    work_zones = relationship("WorkZone", back_populates="block_section")


class Worker(Base):
    __tablename__ = "workers"

    id = Column(String(50), primary_key=True)  # WRK-101
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)  # Gang Maintainer, Keyman, etc.
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=True)
    current_block_section = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="SAFE")  # SAFE, CAUTION, WARNING, CRITICAL, EMERGENCY, DEGRADED_NETWORK
    network_state = Column(String(20), nullable=False, default="ONLINE")  # ONLINE, OFFLINE, DEGRADED
    battery_level = Column(Integer, nullable=False, default=100)
    gps_accuracy_meters = Column(Float, nullable=False, default=2.5)
    position_x = Column(Float, nullable=False, default=450.0)
    position_y = Column(Float, nullable=False, default=140.0)
    current_geom = Column(Geometry("POINT", srid=4326), nullable=True)
    last_location_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    unacknowledged_alert_id = Column(String(50), nullable=True)
    envelope_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", back_populates="worker")
    team = relationship("Team", back_populates="workers")
    locations = relationship("WorkerLocation", back_populates="worker")
    alerts = relationship("Alert", back_populates="worker")


class Train(Base):
    __tablename__ = "trains"

    id = Column(String(50), primary_key=True)  # TRN-204
    number = Column(String(50), nullable=False, index=True)  # 12626
    name = Column(String(255), nullable=False)  # MAS-SBC Express
    line = Column(String(50), nullable=False, default="DOWN")
    current_block_section = Column(String(100), nullable=False, index=True)
    position_x = Column(Float, nullable=False, default=0.0)
    speed_kmh = Column(Float, nullable=False, default=110.0)
    heading = Column(Float, nullable=False, default=90.0)  # degrees 0-360
    direction = Column(String(20), nullable=False, default="EASTBOUND")
    status = Column(String(50), nullable=False, default="APPROACHING")
    current_geom = Column(Geometry("POINT", srid=4326), nullable=True)
    last_position_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    positions = relationship("TrainPosition", back_populates="train")


class WorkZone(Base):
    __tablename__ = "work_zones"

    id = Column(String(50), primary_key=True)  # WZ-402
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    block_section_code = Column(String(100), nullable=False, index=True)
    block_section_id = Column(String(36), ForeignKey("block_sections.id"), nullable=True)
    start_x = Column(Float, nullable=False)
    end_x = Column(Float, nullable=False)
    buffer_zone_meters = Column(Float, nullable=False, default=500.0)
    safety_zone_meters = Column(Float, nullable=False, default=200.0)
    assigned_team_code = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")  # PLANNED, ACTIVE, PAUSED, COMPLETED, CANCELLED
    is_active = Column(Boolean, default=True)
    geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    block_section = relationship("BlockSection", back_populates="work_zones")
    safety_zones = relationship("SafetyZone", back_populates="work_zone")
    refuge_locations = relationship("SafeRefugeLocation", back_populates="work_zone")


class SafetyZone(Base):
    __tablename__ = "safety_zones"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    work_zone_id = Column(String(50), ForeignKey("work_zones.id"), nullable=False)
    name = Column(String(255), nullable=False)
    zone_type = Column(String(50), nullable=False, default="REFUGE_ZONE")  # REFUGE_ZONE, BUFFER_ZONE, DANGER_ZONE
    start_x = Column(Float, nullable=False)
    end_x = Column(Float, nullable=False)
    geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    work_zone = relationship("WorkZone", back_populates="safety_zones")


class SafeRefugeLocation(Base):
    __tablename__ = "safe_refuge_locations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    work_zone_id = Column(String(50), ForeignKey("work_zones.id"), nullable=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # REFUGE-MAS-101
    name = Column(String(255), nullable=False)
    refuge_type = Column(String(50), nullable=False, default="NICHE")  # NICHE, PLATFORM, SIDE_CLEARANCE
    capacity_persons = Column(Integer, nullable=False, default=10)
    position_x = Column(Float, nullable=False, default=0.0)
    position_y = Column(Float, nullable=False, default=0.0)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)
    boundary_geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    work_zone = relationship("WorkZone", back_populates="refuge_locations")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(50), primary_key=True)  # ALT-1001
    worker_id = Column(String(50), ForeignKey("workers.id"), nullable=False, index=True)
    worker_name = Column(String(255), nullable=False)
    train_id = Column(String(50), nullable=False)
    train_name = Column(String(255), nullable=False)
    block_section_code = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False)  # CAUTION, WARNING, CRITICAL, EMERGENCY, SAFE
    time_to_danger_seconds = Column(Integer, nullable=False)
    distance_to_train_meters = Column(Float, nullable=False)
    escalation_tier = Column(String(50), nullable=False)  # WORKER_ACK, TIER_1_SUPERVISOR, TIER_3_CONTROL_ROOM
    required_action = Column(Text, nullable=False)
    is_acknowledged = Column(Boolean, default=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    worker = relationship("Worker", back_populates="alerts")


class NearMiss(Base):
    __tablename__ = "near_misses"

    id = Column(String(50), primary_key=True)  # NM-9012
    occurred_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    train_id = Column(String(50), nullable=False)
    train_speed_kmh = Column(Float, nullable=False)
    worker_id = Column(String(50), nullable=False, index=True)
    worker_name = Column(String(255), nullable=False)
    block_section_code = Column(String(100), nullable=False, index=True)
    min_spatial_clearance_meters = Column(Float, nullable=False)
    ttd_at_ack_seconds = Column(Integer, nullable=False)
    severity = Column(String(50), nullable=False)  # LOW, MODERATE, HIGH, SEVERE
    contributing_factors = Column(JSON, nullable=False)
    location_coords = Column(JSON, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class EmergencyEvent(Base):
    __tablename__ = "emergency_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(100), unique=True, nullable=False, index=True)
    worker_id = Column(String(50), nullable=False, index=True)
    block_section_code = Column(String(100), nullable=False)
    trigger_type = Column(String(50), nullable=False)  # MANUAL_SOS, AUTO_CRITICAL
    status = Column(String(50), nullable=False, default="ACTIVE")
    acknowledged_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class Device(Base):
    __tablename__ = "devices"

    id = Column(String(50), primary_key=True)  # DEV-801
    worker_id = Column(String(50), ForeignKey("workers.id"), nullable=True)
    device_type = Column(String(50), nullable=False, default="HANDHELD_SAFETY_UNIT")
    firmware_version = Column(String(50), nullable=False, default="2.1.0-prod")
    battery_percentage = Column(Integer, nullable=False, default=95)
    network_signal_dbm = Column(Integer, nullable=False, default=-72)
    last_ping_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    status = Column(String(50), nullable=False, default="HEALTHY")
    current_geom = Column(Geometry("POINT", srid=4326), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class DeviceLocation(Base):
    __tablename__ = "device_locations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    device_id = Column(String(50), ForeignKey("devices.id"), nullable=False, index=True)
    worker_id = Column(String(50), ForeignKey("workers.id"), nullable=True, index=True)
    position_x = Column(Float, nullable=False, default=0.0)
    position_y = Column(Float, nullable=False, default=0.0)
    gps_accuracy_meters = Column(Float, nullable=False, default=2.5)
    battery_percentage = Column(Integer, nullable=False, default=95)
    network_signal_dbm = Column(Integer, nullable=False, default=-72)
    source = Column(String(50), nullable=False, default="HARDWARE_UNIT")
    sequence = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(100), unique=True, nullable=False, index=True)
    actor = Column(String(255), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    request_id = Column(String(100), nullable=True)
    correlation_id = Column(String(100), nullable=True, index=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class TrainPosition(Base):
    __tablename__ = "train_positions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    train_id = Column(String(50), ForeignKey("trains.id"), nullable=False, index=True)
    position_x = Column(Float, nullable=False)
    speed_kmh = Column(Float, nullable=False)
    heading = Column(Float, nullable=False, default=90.0)
    direction = Column(String(20), nullable=False, default="EASTBOUND")
    source = Column(String(50), nullable=False, default="SIMULATOR")  # SIMULATOR, TELEMETRY, TEST
    sequence = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)

    train = relationship("Train", back_populates="positions")


class WorkerLocation(Base):
    __tablename__ = "worker_locations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    worker_id = Column(String(50), ForeignKey("workers.id"), nullable=False, index=True)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    gps_accuracy_meters = Column(Float, nullable=False)
    source = Column(String(50), nullable=False, default="SIMULATOR")  # SIMULATOR, MOBILE, TEST
    device_id = Column(String(50), nullable=True)
    sequence = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)

    worker = relationship("Worker", back_populates="locations")


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    worker_id = Column(String(50), ForeignKey("workers.id"), nullable=False)
    work_zone_id = Column(String(50), ForeignKey("work_zones.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False, default="ACTIVE")


class SpatialEvent(Base):
    __tablename__ = "spatial_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(100), nullable=False, index=True)  # WORKER_ENTERED_ZONE, TRAIN_APPROACHING_BLOCK, NEARBY_WORKERS_QUERY
    entity_type = Column(String(50), nullable=False)  # WORKER, TRAIN, WORK_ZONE
    entity_id = Column(String(50), nullable=False, index=True)
    target_type = Column(String(50), nullable=True)  # WORK_ZONE, BLOCK_SECTION, REFUGE
    target_id = Column(String(50), nullable=True, index=True)
    distance_meters = Column(Float, nullable=True)
    details = Column(JSON, nullable=True)
    geom = Column(Geometry("GEOMETRY", srid=4326), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    recipient_role = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# Indexing definitions for performance
Index("idx_alert_worker_ack", Alert.worker_id, Alert.is_acknowledged)
Index("idx_audit_actor_timestamp", AuditLog.actor, AuditLog.timestamp)
