import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from app.models.domain_models import Worker, Train, WorkZone, BlockSection, TrackSegment
from app.services.safety_engine import SafetyEngine
from app.services.alert_service import create_or_update_alert
from app.realtime.connection_manager import connection_manager

logger = logging.getLogger("dost_guardian.simulation_service")


def utc_now():
    return datetime.now(timezone.utc)


class RailwayDigitalTwinSimulator:
    """
    Deterministic Railway Digital Twin Simulation Service.
    Advances synthetic train movements along track segments, evaluates PostGIS spatial relationships,
    and drives real-time safety state transitions.
    """

    @classmethod
    async def process_simulation_tick(cls, db: Session, speed_multiplier: float = 1.0) -> Dict[str, Any]:
        """
        Executes one deterministic simulation step:
        1. Advances Train EXP-12626 along track (X=0 to X=1000).
        2. Updates WGS84 coordinates & PostGIS geometry.
        3. Evaluates SafetyEngine rule-based state transitions for workers.
        4. Broadcasts WebSocket spatial operational update.
        """
        train = db.query(Train).filter(Train.id == "TRN-204").first()
        if not train:
            return {"status": "NO_TRAINS"}

        # Advance position along track (1 unit = 10 meters)
        step = (train.speed_kmh * 0.2 * speed_multiplier) / 3.6
        new_x = train.position_x + step
        if new_x > 1000.0:
            new_x = 0.0  # Loop back to track start

        train.position_x = new_x

        # Calculate synthetic WGS84 coordinate mapped to track position
        base_lng = 80.2700
        base_lat = 13.0820
        lng_offset = (new_x / 1000.0) * 0.0200
        lat_offset = (new_x / 1000.0) * 0.0010
        current_lng = base_lng + lng_offset
        current_lat = base_lat + lat_offset

        train.current_geom = WKTElement(f"POINT({current_lng} {current_lat})", srid=4326)
        train.updated_at = utc_now()
        db.commit()

        # Evaluate safety state against all active workers
        workers = db.query(Worker).all()
        safety_evaluations = []
        alerts_generated = []

        for worker in workers:
            eval_result = SafetyEngine.evaluate_worker_train_safety(
                worker_id=worker.id,
                worker_x=worker.position_x,
                worker_y=worker.position_y,
                worker_gps_accuracy=worker.gps_accuracy_meters,
                train_id=train.id,
                train_number=train.number,
                train_name=train.name,
                train_x=train.position_x,
                train_speed_kmh=train.speed_kmh,
                train_direction=train.direction,
                block_section_code=train.current_block_section,
                network_online=(worker.network_state == "ONLINE"),
            )
            safety_evaluations.append(eval_result)

            # Generate or update alert if in WARNING, CRITICAL, or EMERGENCY state
            if eval_result["state"] in ["WARNING", "CRITICAL", "EMERGENCY"]:
                alert_dict, is_new = create_or_update_alert(
                    db=db,
                    worker_id=worker.id,
                    worker_name=worker.name,
                    train_id=train.id,
                    train_name=train.name,
                    block_section_code=train.current_block_section,
                    state=eval_result["state"],
                    time_to_danger_seconds=eval_result["ttd_seconds"],
                    distance_to_train_meters=eval_result["distance_meters"],
                    escalation_tier=eval_result["escalation_tier"],
                    required_action=eval_result["required_action"],
                )
                alerts_generated.append(alert_dict)

        # Broadcast real-time operational state update via WebSocket
        tick_event = {
            "event_id": f"evt-sim-tick-{int(utc_now().timestamp())}",
            "event_type": "SIMULATION_TICK_UPDATE",
            "occurred_at": utc_now().isoformat(),
            "payload": {
                "train": {
                    "id": train.id,
                    "number": train.number,
                    "position_x": round(train.position_x, 1),
                    "speed_kmh": train.speed_kmh,
                    "lat": current_lat,
                    "lng": current_lng,
                },
                "safety_evaluations": safety_evaluations,
                "alerts": alerts_generated,
            },
        }
        await connection_manager.broadcast(tick_event)

        return {
            "status": "PROCESSED",
            "train_position_x": round(new_x, 1),
            "workers_evaluated": len(workers),
            "active_alerts": len(alerts_generated),
        }
