import logging
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, select
from geoalchemy2 import Geography, Geometry
from geoalchemy2.elements import WKTElement
from app.models.domain_models import (
    Worker,
    Train,
    WorkZone,
    BlockSection,
    TrackSegment,
    SafeRefugeLocation,
    Station,
    SpatialEvent,
    WorkerLocation,
    TrainPosition,
)

logger = logging.getLogger("dost_guardian.spatial_repository")


class SpatialRepository:
    @staticmethod
    def create_point_wkt(lng: float, lat: float) -> str:
        """Returns WKT string for WGS84 Point (lng, lat)."""
        return f"POINT({lng} {lat})"

    @classmethod
    def find_nearby_workers(
        cls,
        db: Session,
        lat: float,
        lng: float,
        radius_meters: float,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Tuple[Worker, float]]:
        """
        Queries workers within radius_meters of (lat, lng) using ST_DWithin on Geography.
        Returns list of tuples: (Worker, distance_in_meters).
        """
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        point_geog = cast(point_geom, Geography)
        worker_geog = cast(Worker.current_geom, Geography)

        distance_expr = func.ST_Distance(worker_geog, point_geog).label("distance_meters")

        query = (
            db.query(Worker, distance_expr)
            .filter(Worker.current_geom.isnot(None))
            .filter(func.ST_DWithin(worker_geog, point_geog, radius_meters))
            .order_by(distance_expr)
            .offset(offset)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def find_nearby_trains(
        cls,
        db: Session,
        lat: float,
        lng: float,
        radius_meters: float,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Tuple[Train, float]]:
        """
        Queries trains within radius_meters of (lat, lng) using ST_DWithin on Geography.
        Returns list of tuples: (Train, distance_in_meters).
        """
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        point_geog = cast(point_geom, Geography)
        train_geog = cast(Train.current_geom, Geography)

        distance_expr = func.ST_Distance(train_geog, point_geog).label("distance_meters")

        query = (
            db.query(Train, distance_expr)
            .filter(Train.current_geom.isnot(None))
            .filter(func.ST_DWithin(train_geog, point_geog, radius_meters))
            .order_by(distance_expr)
            .offset(offset)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def find_workers_in_zone(
        cls,
        db: Session,
        work_zone_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Worker]:
        """
        Determines workers spatially contained/intersecting the work zone polygon.
        Boundary points are considered inside via ST_Intersects.
        """
        zone = db.query(WorkZone).filter(WorkZone.id == work_zone_id).first()
        if not zone or zone.geom is None:
            return []

        query = (
            db.query(Worker)
            .filter(Worker.current_geom.isnot(None))
            .filter(func.ST_Intersects(Worker.current_geom, zone.geom))
            .offset(offset)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def find_trains_in_zone(
        cls,
        db: Session,
        work_zone_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Train]:
        """
        Determines trains spatially contained/intersecting the work zone polygon.
        """
        zone = db.query(WorkZone).filter(WorkZone.id == work_zone_id).first()
        if not zone or zone.geom is None:
            return []

        query = (
            db.query(Train)
            .filter(Train.current_geom.isnot(None))
            .filter(func.ST_Intersects(Train.current_geom, zone.geom))
            .offset(offset)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def find_containing_block(
        cls,
        db: Session,
        lat: float,
        lng: float,
    ) -> Tuple[Optional[BlockSection], List[BlockSection]]:
        """
        Determines which block section contains or is nearest to (lat, lng).
        Returns: (primary_containing_block, candidate_blocks).
        """
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        point_geog = cast(point_geom, Geography)

        # First query corridor polygon containment or line intersection
        direct_matches = (
            db.query(BlockSection)
            .filter(
                (BlockSection.corridor_geom.isnot(None) & func.ST_Intersects(BlockSection.corridor_geom, point_geom))
                | (BlockSection.geom.isnot(None) & func.ST_DWithin(cast(BlockSection.geom, Geography), point_geog, 50.0))
            )
            .all()
        )

        if direct_matches:
            return direct_matches[0], direct_matches

        # Fallback to nearest block section within 500m
        nearest = (
            db.query(BlockSection)
            .filter(BlockSection.geom.isnot(None))
            .order_by(func.ST_Distance(cast(BlockSection.geom, Geography), point_geog))
            .first()
        )
        return nearest, [nearest] if nearest else []

    @classmethod
    def find_nearby_tracks(
        cls,
        db: Session,
        lat: float,
        lng: float,
        radius_meters: float = 500.0,
        limit: int = 20,
    ) -> List[Tuple[TrackSegment, float]]:
        """Find track segments near point (lat, lng)."""
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        point_geog = cast(point_geom, Geography)
        track_geog = cast(TrackSegment.geom, Geography)
        distance_expr = func.ST_Distance(track_geog, point_geog).label("distance_meters")

        query = (
            db.query(TrackSegment, distance_expr)
            .filter(TrackSegment.geom.isnot(None))
            .filter(func.ST_DWithin(track_geog, point_geog, radius_meters))
            .order_by(distance_expr)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def find_nearest_refuge(
        cls,
        db: Session,
        lat: float,
        lng: float,
        limit: int = 5,
    ) -> List[Tuple[SafeRefugeLocation, float]]:
        """
        Returns nearest safe refuge locations to (lat, lng) ordered by KNN geodetic distance.
        """
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        point_geog = cast(point_geom, Geography)
        refuge_geog = cast(SafeRefugeLocation.geom, Geography)
        distance_expr = func.ST_Distance(refuge_geog, point_geog).label("distance_meters")

        query = (
            db.query(SafeRefugeLocation, distance_expr)
            .filter(SafeRefugeLocation.geom.isnot(None))
            .filter(SafeRefugeLocation.is_active.is_(True))
            .order_by(distance_expr)
            .limit(limit)
        )
        return query.all()

    @classmethod
    def update_worker_location(
        cls,
        db: Session,
        worker_id: str,
        lat: float,
        lng: float,
        accuracy_meters: float = 2.5,
        source: str = "SIMULATOR",
        device_id: Optional[str] = None,
    ) -> Tuple[Worker, WorkerLocation]:
        """
        Persists a historical WorkerLocation record and updates Worker.current_geom.
        """
        point_wkt = cls.create_point_wkt(lng, lat)
        wkt_elem = WKTElement(point_wkt, srid=4326)

        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise ValueError(f"Worker {worker_id} not found")

        # Create historical location
        loc = WorkerLocation(
            worker_id=worker_id,
            position_x=worker.position_x,
            position_y=worker.position_y,
            gps_accuracy_meters=accuracy_meters,
            source=source,
            device_id=device_id,
            geom=wkt_elem,
        )
        db.add(loc)

        # Update current worker geometry
        worker.current_geom = wkt_elem
        worker.gps_accuracy_meters = accuracy_meters
        db.commit()
        db.refresh(worker)
        return worker, loc

    @classmethod
    def update_train_position(
        cls,
        db: Session,
        train_id: str,
        lat: float,
        lng: float,
        speed_kmh: float,
        heading: float = 90.0,
        source: str = "SIMULATOR",
    ) -> Tuple[Train, TrainPosition]:
        """
        Persists a historical TrainPosition record and updates Train.current_geom.
        """
        point_wkt = cls.create_point_wkt(lng, lat)
        wkt_elem = WKTElement(point_wkt, srid=4326)

        train = db.query(Train).filter(Train.id == train_id).first()
        if not train:
            raise ValueError(f"Train {train_id} not found")

        pos = TrainPosition(
            train_id=train_id,
            position_x=train.position_x,
            speed_kmh=speed_kmh,
            heading=heading,
            direction=train.direction,
            source=source,
            geom=wkt_elem,
        )
        db.add(pos)

        train.current_geom = wkt_elem
        train.speed_kmh = speed_kmh
        train.heading = heading
        db.commit()
        db.refresh(train)
        return train, pos
