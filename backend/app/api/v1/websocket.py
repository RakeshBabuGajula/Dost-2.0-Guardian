import json
import logging
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.realtime.connection_manager import connection_manager
from app.schemas.realtime import SnapshotData
from app.services.worker_service import get_all_workers
from app.services.train_service import get_all_trains
from app.services.alert_service import get_all_alerts

router = APIRouter(tags=["Real-Time WebSockets"])
logger = logging.getLogger("dost_guardian.websocket")


@router.websocket("/ws/operations")
async def websocket_operations_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    db = SessionLocal()
    try:
        # Build initial snapshot payload for newly connected client (Section 18)
        workers = get_all_workers(db)
        trains = get_all_trains(db)
        alerts = get_all_alerts(db)

        snapshot = SnapshotData(
            snapshot_version=1,
            last_event_sequence=connection_manager.sequence_counter,
            workers=workers,
            trains=trains,
            work_zones=[],
            alerts=alerts,
            near_misses=[],
            system_health={"status": "HEALTHY", "timestamp": datetime.utcnow().isoformat()},
        )
        await connection_manager.send_snapshot(websocket, snapshot)

        while True:
            data_text = await websocket.receive_text()
            try:
                msg = json.loads(data_text)
                msg_type = msg.get("type")

                if msg_type == "PING":
                    await connection_manager.send_personal_message(
                        {"type": "HEARTBEAT", "timestamp": datetime.utcnow().isoformat()},
                        websocket,
                    )
                elif msg_type == "SUBSCRIBE":
                    await connection_manager.send_personal_message(
                        {"type": "SUBSCRIPTION_ACK", "status": "SUBSCRIBED"},
                        websocket,
                    )
                elif msg_type == "ACK":
                    logger.debug(f"Received ACK from client: {msg.get('sequence')}")
            except Exception as parse_err:
                logger.warning(f"Error parsing WebSocket frame: {parse_err}")
                await connection_manager.send_personal_message(
                    {"type": "ERROR", "error": "Invalid JSON frame"},
                    websocket,
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    finally:
        db.close()
