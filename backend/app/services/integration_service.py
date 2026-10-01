import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from app.models.domain_models import (
    Train, TrainPosition, BlockSection, WorkZone, EmergencyEvent, AuditLog, SpatialEvent
)
from app.schemas.integration import (
    TrainPositionIngest, BlockStatusIngest, WorkOrderIngest, EmergencyIngest, NormalizedIntegrationResult
)

class IntegrationAdapterService:
    def __init__(self, db: Session):
        self.db = db

    def process_train_position_ingest(
        self, payload: TrainPositionIngest, correlation_id: str
    ) -> NormalizedIntegrationResult:
        """
        Normalizes external train telemetry into DOST Guardian PostGIS model.
        Evaluates data freshness; marks as DEGRADED if timestamp is stale (> 60s).
        """
        warnings = []
        status = "ACCEPTED"

        # 1. Parse and validate timestamp
        try:
            ts_str = payload.timestamp.replace("Z", "+00:00")
            parsed_ts = datetime.fromisoformat(ts_str)
        except Exception:
            parsed_ts = datetime.now(timezone.utc)
            warnings.append("Invalid timestamp format; defaulted to current UTC time")
            status = "DEGRADED"

        now = datetime.now(timezone.utc)
        age_seconds = (now - parsed_ts).total_seconds()
        if age_seconds > 60:
            warnings.append(f"Stale telemetry detected (age: {round(age_seconds, 1)}s > 60s)")
            status = "DEGRADED"

        # 2. Validate WGS84 coordinate boundaries for Indian Railways MAS-AJJ corridor
        lat, lng = payload.latitude, payload.longitude
        if not (8.0 <= lat <= 37.0 and 68.0 <= lng <= 97.0):
            warnings.append(f"Coordinates ({lat}, {lng}) outside canonical Indian geographical bounds")
            status = "DEGRADED"

        # 3. Create or update Train entity
        train = self.db.query(Train).filter(Train.id == payload.train_id).first()
        wkt_geom = f"POINT({lng} {lat})"

        if not train:
            train = Train(
                id=payload.train_id,
                number=payload.number,
                name=payload.name,
                line=payload.line,
                current_block_section=payload.block_section_code,
                position_x=float(lng * 100.0),
                speed_kmh=payload.speed_kmh,
                heading=payload.heading_degrees,
                direction=payload.direction,
                status="APPROACHING" if payload.speed_kmh > 0 else "STOPPED",
                current_geom=WKTElement(wkt_geom, srid=4326),
                last_position_at=parsed_ts,
            )
            self.db.add(train)
        else:
            train.speed_kmh = payload.speed_kmh
            train.heading = payload.heading_degrees
            train.current_block_section = payload.block_section_code
            train.current_geom = WKTElement(wkt_geom, srid=4326)
            train.last_position_at = parsed_ts
            train.status = "APPROACHING" if payload.speed_kmh > 0 else "STOPPED"

        # 4. Record TrainPosition trajectory point
        pos_record = TrainPosition(
            id=str(uuid.uuid4()),
            train_id=payload.train_id,
            position_x=float(lng * 100.0),
            speed_kmh=payload.speed_kmh,
            heading=payload.heading_degrees,
            direction=payload.direction,
            source=f"EXTERNAL_ADAPTER:{payload.source_system_id}",
            timestamp=parsed_ts,
            geom=WKTElement(wkt_geom, srid=4326),
        )
        self.db.add(pos_record)

        # 5. Record Integration Audit Log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            event_id=f"evt-ingest-train-{uuid.uuid4().hex[:8]}",
            actor=f"SYSTEM:{payload.source_system_id}",
            action="INGEST_TRAIN_TELEMETRY",
            target=payload.train_id,
            request_id=correlation_id,
            correlation_id=correlation_id,
            details={
                "status": status,
                "speed_kmh": payload.speed_kmh,
                "block_section": payload.block_section_code,
                "warnings": warnings,
            }
        )
        self.db.add(audit)
        self.db.commit()

        return NormalizedIntegrationResult(
            correlation_id=correlation_id,
            status=status,
            entity_type="TRAIN",
            entity_id=payload.train_id,
            warnings=warnings,
            normalized_data={
                "train_id": payload.train_id,
                "number": payload.number,
                "speed_kmh": payload.speed_kmh,
                "block_section": payload.block_section_code,
                "coordinates": {"lat": lat, "lng": lng},
                "status": status,
            },
            timestamp=now.isoformat(),
        )

    def process_block_status_ingest(
        self, payload: BlockStatusIngest, correlation_id: str
    ) -> NormalizedIntegrationResult:
        """Normalizes external block section status update."""
        warnings = []
        status = "ACCEPTED"

        block = self.db.query(BlockSection).filter(BlockSection.code == payload.block_section_code).first()
        if not block:
            block = BlockSection(
                id=str(uuid.uuid4()),
                code=payload.block_section_code,
                name=f"Block Section {payload.block_section_code}",
                line_type=payload.line_type,
                start_km=0.0,
                end_km=5.0,
                speed_limit_kmh=payload.speed_limit_kmh,
                status=payload.status,
            )
            self.db.add(block)
        else:
            block.status = payload.status
            block.speed_limit_kmh = payload.speed_limit_kmh

        audit = AuditLog(
            id=str(uuid.uuid4()),
            event_id=f"evt-ingest-block-{uuid.uuid4().hex[:8]}",
            actor=f"SYSTEM:{payload.source_system_id}",
            action="INGEST_BLOCK_STATUS",
            target=payload.block_section_code,
            request_id=correlation_id,
            correlation_id=correlation_id,
            details={"status": payload.status, "speed_limit_kmh": payload.speed_limit_kmh}
        )
        self.db.add(audit)
        self.db.commit()

        return NormalizedIntegrationResult(
            correlation_id=correlation_id,
            status=status,
            entity_type="BLOCK_SECTION",
            entity_id=payload.block_section_code,
            warnings=warnings,
            normalized_data={
                "block_section_code": payload.block_section_code,
                "status": payload.status,
                "speed_limit_kmh": payload.speed_limit_kmh,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def process_work_order_ingest(
        self, payload: WorkOrderIngest, correlation_id: str
    ) -> NormalizedIntegrationResult:
        """Normalizes external work zone order into DOST Guardian model."""
        wz = self.db.query(WorkZone).filter(WorkZone.id == payload.work_zone_id).first()
        wkt_geom = "POLYGON((80.270 13.080, 80.280 13.080, 80.280 13.085, 80.270 13.085, 80.270 13.080))"

        if not wz:
            wz = WorkZone(
                id=payload.work_zone_id,
                name=payload.name,
                block_section_code=payload.block_section_code,
                start_x=400.0,
                end_x=600.0,
                buffer_zone_meters=payload.buffer_zone_meters,
                safety_zone_meters=payload.safety_zone_meters,
                assigned_team_code=payload.assigned_team_code,
                status="ACTIVE",
                geom=WKTElement(wkt_geom, srid=4326),
            )
            self.db.add(wz)

        audit = AuditLog(
            id=str(uuid.uuid4()),
            event_id=f"evt-ingest-wz-{uuid.uuid4().hex[:8]}",
            actor=f"SYSTEM:{payload.source_system_id}",
            action="INGEST_WORK_ORDER",
            target=payload.work_zone_id,
            request_id=correlation_id,
            correlation_id=correlation_id,
            details={"block_section": payload.block_section_code, "team": payload.assigned_team_code}
        )
        self.db.add(audit)
        self.db.commit()

        return NormalizedIntegrationResult(
            correlation_id=correlation_id,
            status="ACCEPTED",
            entity_type="WORK_ZONE",
            entity_id=payload.work_zone_id,
            warnings=[],
            normalized_data={
                "work_zone_id": payload.work_zone_id,
                "name": payload.name,
                "block_section": payload.block_section_code,
                "team": payload.assigned_team_code,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def process_emergency_ingest(
        self, payload: EmergencyIngest, correlation_id: str
    ) -> NormalizedIntegrationResult:
        """Normalizes external track emergency notification."""
        emg = self.db.query(EmergencyEvent).filter(EmergencyEvent.event_id == payload.event_id).first()
        if not emg:
            emg = EmergencyEvent(
                id=str(uuid.uuid4()),
                event_id=payload.event_id,
                worker_id=payload.worker_id,
                block_section_code=payload.block_section_code,
                trigger_type=payload.trigger_type,
                status="ACTIVE",
            )
            self.db.add(emg)

        audit = AuditLog(
            id=str(uuid.uuid4()),
            event_id=f"evt-ingest-emg-{uuid.uuid4().hex[:8]}",
            actor=f"SYSTEM:{payload.source_system_id}",
            action="INGEST_EXTERNAL_EMERGENCY",
            target=payload.event_id,
            request_id=correlation_id,
            correlation_id=correlation_id,
            details={"worker_id": payload.worker_id, "block_section": payload.block_section_code}
        )
        self.db.add(audit)
        self.db.commit()

        return NormalizedIntegrationResult(
            correlation_id=correlation_id,
            status="ACCEPTED",
            entity_type="EMERGENCY_EVENT",
            entity_id=payload.event_id,
            warnings=[],
            normalized_data={
                "event_id": payload.event_id,
                "worker_id": payload.worker_id,
                "block_section": payload.block_section_code,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def run_simulated_external_provider_tick(self) -> Dict[str, Any]:
        """Runs a tick of the simulated external railway provider for integration testing."""
        corr_id = f"corr-sim-{uuid.uuid4().hex[:8]}"

        payload = TrainPositionIngest(
            train_id="TRN-EXT-204",
            number="12626",
            name="MAS-SBC Express (External Ingest)",
            line="DOWN",
            block_section_code="MAS-AJJ-DOWN-120",
            latitude=13.0827,
            longitude=80.2707,
            speed_kmh=108.5,
            heading_degrees=90.0,
            direction="EASTBOUND",
            source_system_id="SIMULATED-RAILWAY-CONTROL-CENTER",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        res = self.process_train_position_ingest(payload, corr_id)
        return {
            "simulation_tick": "COMPLETED",
            "correlation_id": corr_id,
            "provider": "SIMULATED-RAILWAY-CONTROL-CENTER",
            "result": res.dict(),
        }
