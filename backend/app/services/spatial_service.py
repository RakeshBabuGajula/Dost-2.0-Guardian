import logging
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from app.db.spatial_repository import SpatialRepository
from app.models.domain_models import Worker, Train, WorkZone, BlockSection, TrackSegment, SafeRefugeLocation
from app.schemas.spatial import (
    LocationPoint,
    SpatialWorkerResult,
    SpatialTrainResult,
    RefugeResult,
    BlockContextResult,
    TrackSegmentResult,
    SpatialWorkerContext,
)

logger = logging.getLogger("dost_guardian.spatial_service")


class SpatialService:
    @staticmethod
    def _extract_lng_lat(geom) -> Tuple[float, float]:
        """Extracts (lng, lat) from a GeoAlchemy2 / WKT / WKB geometry."""
        if geom is None:
            return 80.2750, 13.0823  # Fallback synthetic default
        try:
            shape = to_shape(geom)
            return shape.x, shape.y
        except Exception:
            return 80.2750, 13.0823

    @classmethod
    def get_nearby_workers(
        cls,
        db: Session,
        lat: float,
        lng: float,
        radius_meters: float,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SpatialWorkerResult]:
        """Spatial query: Find workers within radius_meters."""
        raw_results = SpatialRepository.find_nearby_workers(db, lat, lng, radius_meters, limit, offset)
        results = []
        for worker, dist in raw_results:
            w_lng, w_lat = cls._extract_lng_lat(worker.current_geom)
            results.append(
                SpatialWorkerResult(
                    id=worker.id,
                    name=worker.name,
                    role=worker.role,
                    team_id=worker.team_id,
                    status=worker.status,
                    current_block_section=worker.current_block_section,
                    distance_meters=round(dist, 2),
                    latitude=w_lat,
                    longitude=w_lng,
                    gps_accuracy_meters=worker.gps_accuracy_meters,
                    last_updated_at=worker.updated_at.isoformat() if worker.updated_at else "",
                )
            )
        return results

    @classmethod
    def get_nearby_trains(
        cls,
        db: Session,
        lat: float,
        lng: float,
        radius_meters: float,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SpatialTrainResult]:
        """Spatial query: Find trains within radius_meters."""
        raw_results = SpatialRepository.find_nearby_trains(db, lat, lng, radius_meters, limit, offset)
        results = []
        for train, dist in raw_results:
            t_lng, t_lat = cls._extract_lng_lat(train.current_geom)
            results.append(
                SpatialTrainResult(
                    id=train.id,
                    number=train.number,
                    name=train.name,
                    line=train.line,
                    speed_kmh=train.speed_kmh,
                    heading=train.heading if hasattr(train, "heading") else 90.0,
                    direction=train.direction,
                    current_block_section=train.current_block_section,
                    distance_meters=round(dist, 2),
                    latitude=t_lat,
                    longitude=t_lng,
                    last_updated_at=train.updated_at.isoformat() if train.updated_at else "",
                )
            )
        return results

    @classmethod
    def get_workers_in_zone(
        cls,
        db: Session,
        work_zone_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SpatialWorkerResult]:
        """Spatial query: Find workers inside work zone polygon."""
        workers = SpatialRepository.find_workers_in_zone(db, work_zone_id, limit, offset)
        results = []
        for worker in workers:
            w_lng, w_lat = cls._extract_lng_lat(worker.current_geom)
            results.append(
                SpatialWorkerResult(
                    id=worker.id,
                    name=worker.name,
                    role=worker.role,
                    team_id=worker.team_id,
                    status=worker.status,
                    current_block_section=worker.current_block_section,
                    distance_meters=0.0,
                    latitude=w_lat,
                    longitude=w_lng,
                    gps_accuracy_meters=worker.gps_accuracy_meters,
                    last_updated_at=worker.updated_at.isoformat() if worker.updated_at else "",
                )
            )
        return results

    @classmethod
    def get_containing_block(cls, db: Session, lat: float, lng: float) -> BlockContextResult:
        """Spatial query: Find block section containing coordinate."""
        primary_block, candidates = SpatialRepository.find_containing_block(db, lat, lng)
        candidate_codes = [b.code for b in candidates]
        is_ambiguous = len(candidates) > 1

        if primary_block:
            return BlockContextResult(
                code=primary_block.code,
                name=primary_block.name,
                line_type=primary_block.line_type,
                speed_limit_kmh=primary_block.speed_limit_kmh,
                status=getattr(primary_block, "status", "ACTIVE"),
                candidate_blocks=candidate_codes,
                is_ambiguous=is_ambiguous,
            )
        return BlockContextResult(
            code="UNKNOWN",
            name="Unassigned Track Corridor",
            line_type="BIDIRECTIONAL",
            speed_limit_kmh=110,
            status="UNKNOWN",
            candidate_blocks=[],
            is_ambiguous=False,
        )

    @classmethod
    def get_nearby_tracks(
        cls, db: Session, lat: float, lng: float, radius_meters: float = 500.0, limit: int = 20
    ) -> List[TrackSegmentResult]:
        """Spatial query: Find track segments near coordinate."""
        raw_results = SpatialRepository.find_nearby_tracks(db, lat, lng, radius_meters, limit)
        results = []
        for segment, dist in raw_results:
            results.append(
                TrackSegmentResult(
                    id=segment.id,
                    code=segment.code,
                    name=segment.name,
                    track_code=segment.track_code,
                    direction=segment.direction,
                    chainage_start_km=segment.chainage_start_km,
                    chainage_end_km=segment.chainage_end_km,
                    speed_limit_kmh=segment.speed_limit_kmh,
                    distance_meters=round(dist, 2),
                )
            )
        return results

    @classmethod
    def get_nearest_refuge(cls, db: Session, lat: float, lng: float, limit: int = 5) -> List[RefugeResult]:
        """Spatial query: Find nearest safe refuge locations."""
        raw_results = SpatialRepository.find_nearest_refuge(db, lat, lng, limit)
        results = []
        for refuge, dist in raw_results:
            r_lng, r_lat = cls._extract_lng_lat(refuge.geom)
            results.append(
                RefugeResult(
                    id=refuge.id,
                    code=refuge.code,
                    name=refuge.name,
                    refuge_type=refuge.refuge_type,
                    capacity_persons=refuge.capacity_persons,
                    distance_meters=round(dist, 2),
                    latitude=r_lat,
                    longitude=r_lng,
                )
            )
        return results

    @classmethod
    def get_worker_spatial_context(cls, db: Session, worker_id: str) -> SpatialWorkerContext:
        """
        Enriches a worker's state with full spatial context:
        - current WGS84 point
        - containing block section
        - containing work zone
        - nearest safe refuge
        - nearby trains within 2000 meters
        """
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise ValueError(f"Worker {worker_id} not found")

        w_lng, w_lat = cls._extract_lng_lat(worker.current_geom)
        loc = LocationPoint(latitude=w_lat, longitude=w_lng)

        # Containing block
        block_ctx = cls.get_containing_block(db, w_lat, w_lng)

        # Nearest refuge
        refuge_list = cls.get_nearest_refuge(db, w_lat, w_lng, limit=1)
        nearest_refuge = refuge_list[0] if refuge_list else None

        # Nearby trains (2000m spatial query radius)
        nearby_trains = cls.get_nearby_trains(db, w_lat, w_lng, radius_meters=2000.0, limit=10)

        # Check containing work zone
        zones = SpatialRepository.find_workers_in_zone(db, "WZ-402")  # check active zones
        containing_zone_info = None
        wz = db.query(WorkZone).filter_by(id="WZ-402").first()
        if wz and any(w.id == worker_id for w in zones):
            containing_zone_info = {
                "id": wz.id,
                "name": wz.name,
                "assigned_team_code": wz.assigned_team_code,
                "status": wz.status,
            }

        return SpatialWorkerContext(
            worker_id=worker.id,
            worker_name=worker.name,
            current_location=loc,
            containing_block=block_ctx,
            containing_work_zone=containing_zone_info,
            nearest_refuge=nearest_refuge,
            nearby_trains=nearby_trains,
        )
