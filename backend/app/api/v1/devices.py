from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device import DeviceResponse
from app.models.domain_models import Device

router = APIRouter(prefix="/devices", tags=["Handheld Devices Telematics"])


@router.get("", response_model=List[DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    """Retrieve handheld safety units battery, signal, and firmware health status."""
    devices = db.query(Device).all()
    return [
        {
            "id": dev.id,
            "workerId": dev.worker_id,
            "deviceType": dev.device_type,
            "firmwareVersion": dev.firmware_version,
            "batteryPercentage": dev.battery_percentage,
            "networkSignalDbm": dev.network_signal_dbm,
            "lastPingAt": dev.last_ping_at.isoformat(),
            "status": dev.status,
        }
        for dev in devices
    ]
