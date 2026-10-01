import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.domain_models import NearMiss, Worker, Train
from app.audit.audit_logger import log_audit_event
from geoalchemy2.elements import WKTElement

logger = logging.getLogger("dost_guardian.near_miss_service")


def utc_now():
    return datetime.now(timezone.utc)


def format_near_miss_to_schema(nm: NearMiss) -> dict:
    return {
        "id": nm.id,
        "occurredAt": nm.occurred_at.isoformat() if isinstance(nm.occurred_at, datetime) else str(nm.occurred_at),
        "trainId": nm.train_id,
        "trainSpeedKmh": nm.train_speed_kmh,
        "workerId": nm.worker_id,
        "workerName": nm.worker_name,
        "blockSectionCode": nm.block_section_code,
        "minSpatialClearanceMeters": nm.min_spatial_clearance_meters,
        "ttdAtAckSeconds": nm.ttd_at_ack_seconds,
        "severity": nm.severity,
        "contributingFactors": nm.contributing_factors,
        "locationCoords": nm.location_coords,
    }


def get_all_near_misses(db: Session) -> List[dict]:
    items = db.query(NearMiss).order_by(NearMiss.occurred_at.desc()).all()
    return [format_near_miss_to_schema(nm) for nm in items]


def record_near_miss(
    db: Session,
    worker_id: str,
    worker_name: str,
    train_id: str,
    train_speed_kmh: float,
    block_section_code: str,
    min_clearance_meters: float,
    ttd_seconds: int,
    severity: str = "MODERATE",
    contributing_factors: Optional[List[str]] = None,
    lat: float = 13.0823,
    lng: float = 80.2750,
) -> dict:
    """
    Records a spatial near-miss incident card in the authoritative database.
    """
    if contributing_factors is None:
        contributing_factors = ["Track Curve Blind Spot", "Acoustic Attenuation"]

    nm_id = f"NM-{int(utc_now().timestamp())}"
    point_wkt = f"POINT({lng} {lat})"

    nm = NearMiss(
        id=nm_id,
        occurred_at=utc_now(),
        train_id=train_id,
        train_speed_kmh=train_speed_kmh,
        worker_id=worker_id,
        worker_name=worker_name,
        block_section_code=block_section_code,
        min_spatial_clearance_meters=min_clearance_meters,
        ttd_at_ack_seconds=ttd_seconds,
        severity=severity,
        contributing_factors=contributing_factors,
        location_coords={"x": 450.0, "y": 140.0, "lat": lat, "lng": lng},
        geom=WKTElement(point_wkt, srid=4326),
    )
    db.add(nm)
    db.commit()
    db.refresh(nm)

    log_audit_event(
        db=db,
        actor="SYSTEM_SAFETY_ENGINE",
        action="NEAR_MISS_RECORDED",
        target=f"near_miss:{nm_id}",
        details={
            "worker_id": worker_id,
            "train_id": train_id,
            "min_clearance": min_clearance_meters,
            "severity": severity,
        },
    )

    return format_near_miss_to_schema(nm)
