import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
from app.schemas.realtime import WebSocketMessage, SnapshotData

logger = logging.getLogger("dost_guardian.websocket")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.sequence_counter: int = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to client: {e}")
            self.disconnect(websocket)

    async def broadcast(self, event_envelope: Dict[str, Any]):
        self.sequence_counter += 1
        message = {
            "type": "EVENT",
            "sequence": self.sequence_counter,
            "timestamp": event_envelope.get("occurred_at"),
            "payload": event_envelope,
        }
        json_payload = json.dumps(message)

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json_payload)
            except Exception as e:
                logger.error(f"Error broadcasting WebSocket message: {e}")
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    async def send_snapshot(self, websocket: WebSocket, snapshot_data: SnapshotData):
        message = {
            "type": "SNAPSHOT",
            "sequence": self.sequence_counter,
            "timestamp": snapshot_data.system_health.get("timestamp"),
            "payload": snapshot_data.model_dump(),
        }
        await self.send_personal_message(message, websocket)


connection_manager = ConnectionManager()
