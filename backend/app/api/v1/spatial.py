import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.security.auth import get_current_user
from app.services.spatial_service import SpatialService
from app.schemas.spatial import (
    SpatialWorkerResult,
    SpatialTrainResult,
    RefugeResult,
    BlockContextResult,
    TrackSegmentResult,
    SpatialWorkerContext,
    PaginatedSpatialResult,
)

logger = logging.getLogger("dost_guardian.api.spatial")

router = APIRouter(prefix="/spatial", tags=["geospatial"])


def validate_coordinates(lat: float, lng: float):
    """Validates WGS84 latitude/longitude ranges explicitly."""
    if not (-90.0 <= lat <= 90.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid latitude value {lat}. Latitude must be between -90.0 and 90.0 degrees.",
        )
    if not (-180.0 <= lng <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid longitude value {lng}. Longitude must be between -180.0 and 180.0 degrees.",
        )


@router.get("/workers/nearby", response_model=PaginatedSpatialResult)
def get_nearby_workers(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Center latitude (WGS84)"),
    lng: float = Query(..., ge=-180.0, le=180.0, description="Center longitude (WGS84)"),
    radius_meters: float = Query(500.0, gt=0.0, le=50000.0, description="Spatial query radius in meters"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Returns active workers within specified radius_meters of (lat, lng).
    Informational spatial operation only - not a certified safety decision.
    """
    validate_coordinates(lat, lng)
    workers = SpatialService.get_nearby_workers(db, lat, lng, radius_meters, limit, offset)
    return PaginatedSpatialResult(
        total_count=len(workers),
        limit=limit,
        offset=offset,
        items=workers,
    )


@router.get("/trains/nearby", response_model=PaginatedSpatialResult)
def get_nearby_trains(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Center latitude (WGS84)"),
    lng: float = Query(..., ge=-180.0, le=180.0, description="Center longitude (WGS84)"),
    radius_meters: float = Query(2000.0, gt=0.0, le=100000.0, description="Spatial query radius in meters"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Returns active trains within specified radius_meters of (lat, lng).
    Informational spatial operation only - not a certified safety decision.
    """
    validate_coordinates(lat, lng)
    trains = SpatialService.get_nearby_trains(db, lat, lng, radius_meters, limit, offset)
    return PaginatedSpatialResult(
        total_count=len(trains),
        limit=limit,
        offset=offset,
        items=trains,
    )


@router.get("/work-zones/{work_zone_id}/workers", response_model=PaginatedSpatialResult)
def get_workers_in_work_zone(
    work_zone_id: str,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Returns workers spatially contained or intersecting the work zone polygon.
    """
    workers = SpatialService.get_workers_in_zone(db, work_zone_id, limit, offset)
    return PaginatedSpatialResult(
        total_count=len(workers),
        limit=limit,
        offset=offset,
        items=workers,
    )


@router.get("/blocks/containing-point", response_model=BlockContextResult)
def get_containing_block(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lng: float = Query(..., ge=-180.0, le=180.0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Determines which block section contains or is nearest to (lat, lng).
    """
    validate_coordinates(lat, lng)
    return SpatialService.get_containing_block(db, lat, lng)


@router.get("/tracks/nearby", response_model=List[TrackSegmentResult])
def get_nearby_tracks(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lng: float = Query(..., ge=-180.0, le=180.0),
    radius_meters: float = Query(500.0, gt=0.0, le=5000.0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Returns railway track segments within radius_meters.
    """
    validate_coordinates(lat, lng)
    return SpatialService.get_nearby_tracks(db, lat, lng, radius_meters, limit)


@router.get("/refuges/nearest", response_model=List[RefugeResult])
def get_nearest_refuges(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lng: float = Query(..., ge=-180.0, le=180.0),
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Query: Returns nearest configured safe refuge locations to (lat, lng).
    """
    validate_coordinates(lat, lng)
    return SpatialService.get_nearest_refuge(db, lat, lng, limit)


@router.get("/workers/{worker_id}/context", response_model=SpatialWorkerContext)
def get_worker_spatial_context(
    worker_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Spatial Context Query: Returns complete spatial enrichment context for worker (block, work zone, refuge, nearby trains).
    """
    try:
        return SpatialService.get_worker_spatial_context(db, worker_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
