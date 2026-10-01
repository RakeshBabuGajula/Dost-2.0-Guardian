from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain_models import Worker
from app.schemas.worker import WorkerBase, WorkerEnvelopeSchema, WorkerPositionSchema


def format_worker_to_schema(worker: Worker) -> dict:
    env_data = worker.envelope_data or {
        "radiusMeters": 500,
        "gpsUncertaintyBufferMeters": worker.gps_accuracy_meters,
        "trackGeometryBufferMeters": 50,
        "isExpandedDueToGps": worker.gps_accuracy_meters > 15,
    }
    return {
        "id": worker.id,
        "name": worker.name,
        "role": worker.role,
        "currentBlockSection": worker.current_block_section,
        "status": worker.status,
        "networkState": worker.network_state,
        "batteryLevel": worker.battery_level,
        "gpsAccuracyMeters": worker.gps_accuracy_meters,
        "position": {"x": worker.position_x, "y": worker.position_y},
        "unacknowledgedAlertId": worker.unacknowledged_alert_id,
        "envelope": env_data,
    }


def get_all_workers(db: Session) -> List[dict]:
    workers = db.query(Worker).all()
    return [format_worker_to_schema(w) for w in workers]


def get_worker_by_id(db: Session, worker_id: str) -> Optional[dict]:
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        return None
    return format_worker_to_schema(worker)
