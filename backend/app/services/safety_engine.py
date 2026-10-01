import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.domain_models import Worker, Train, WorkZone, BlockSection, Alert, NearMiss, SafeRefugeLocation

logger = logging.getLogger("dost_guardian.safety_engine")


class OperationalSafetyConfig:
    """Centralized configurable operational parameters (Not certified safety thresholds)."""
    BASE_ENVELOPE_RADIUS_METERS: float = 500.0
    TRACK_GEOMETRY_BUFFER_METERS: float = 50.0
    DEFAULT_SPEED_KMH: float = 110.0

    # Operational Time-To-Danger (TTD) windows in seconds
    TTD_ADVISORY_SECONDS: int = 300   # 5 mins
    TTD_WARNING_SECONDS: int = 180    # 3 mins
    TTD_CRITICAL_SECONDS: int = 90     # 1.5 mins
    TTD_EMERGENCY_SECONDS: int = 30    # 30 secs

    # Escalation policy parameters (unacknowledged alert timeout seconds)
    ESCALATION_SUPERVISOR_TIMEOUT_SEC: int = 10
    ESCALATION_CONTROL_ROOM_TIMEOUT_SEC: int = 20

    # Clearance threshold for near-miss logging (meters)
    NEAR_MISS_CLEARANCE_THRESHOLD_METERS: float = 3.0


class SafetyEngine:
    """
    Deterministic rule-based Railway Worker Safety Engine.
    Strictly NO non-deterministic AI / LLM logic for safety state calculations.
    """

    @staticmethod
    def calculate_dynamic_envelope(
        base_radius_meters: float = OperationalSafetyConfig.BASE_ENVELOPE_RADIUS_METERS,
        gps_accuracy_meters: float = 2.5,
        track_buffer_meters: float = OperationalSafetyConfig.TRACK_GEOMETRY_BUFFER_METERS,
    ) -> Dict[str, Any]:
        """
        Computes dynamic worker safety envelope radius based on GPS uncertainty.
        If GPS accuracy degrades (>10m), envelope expands proportionally.
        """
        is_expanded = gps_accuracy_meters > 10.0
        uncertainty_expansion = gps_accuracy_meters * 5.0 if is_expanded else gps_accuracy_meters
        total_radius = base_radius_meters + uncertainty_expansion + track_buffer_meters

        return {
            "radiusMeters": round(total_radius, 1),
            "gpsUncertaintyBufferMeters": round(gps_accuracy_meters, 1),
            "trackGeometryBufferMeters": round(track_buffer_meters, 1),
            "isExpandedDueToGps": is_expanded,
        }

    @staticmethod
    def calculate_time_to_danger(
        distance_meters: float,
        train_speed_kmh: float,
    ) -> Tuple[int, str]:
        """
        Calculates Time-To-Danger (TTD) in seconds given distance and speed.
        Returns tuple: (ttd_seconds, formatted_human_readable_str).
        """
        if train_speed_kmh <= 0.0 or distance_meters <= 0.0:
            return 0, "00:00"

        speed_mps = (train_speed_kmh * 1000.0) / 3600.0
        ttd_seconds = int(distance_meters / speed_mps)

        minutes = ttd_seconds // 60
        seconds = ttd_seconds % 60
        formatted = f"{minutes:02d}:{seconds:02d}"
        return ttd_seconds, formatted

    @classmethod
    def evaluate_worker_train_safety(
        cls,
        worker_id: str,
        worker_x: float,
        worker_y: float,
        worker_gps_accuracy: float,
        train_id: str,
        train_number: str,
        train_name: str,
        train_x: float,
        train_speed_kmh: float,
        train_direction: str,
        block_section_code: str,
        network_online: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluates worker & train operational safety relationship deterministically.
        Returns safety state evaluation dictionary.
        """
        # Distance along track line (1 track unit = 10 meters)
        distance_track_units = worker_x - train_x
        distance_meters = max(0.0, distance_track_units * 10.0)

        envelope = cls.calculate_dynamic_envelope(gps_accuracy_meters=worker_gps_accuracy)
        ttd_seconds, ttd_formatted = cls.calculate_time_to_danger(distance_meters, train_speed_kmh)

        # Check network degradation
        if not network_online:
            return {
                "worker_id": worker_id,
                "status": "DEGRADED_NETWORK",
                "state": "DEGRADED_NETWORK",
                "distance_meters": distance_meters,
                "ttd_seconds": ttd_seconds,
                "ttd_formatted": ttd_formatted,
                "required_action": "NETWORK DEGRADED - MAINTAIN LOCAL BLE MESH VIGILANCE",
                "envelope": envelope,
                "escalation_tier": "TIER_0_WORKER",
            }

        # Determine safety state transitions based on TTD & distance
        if distance_track_units <= 0:
            # Train has passed worker location
            status = "SAFE"
            action = "TRAIN PASSED - MAINTAIN TRACK AWARENESS"
            tier = "TIER_0_WORKER"
        elif ttd_seconds <= OperationalSafetyConfig.TTD_EMERGENCY_SECONDS or distance_meters <= 100:
            status = "EMERGENCY"
            action = "IMMEDIATE EVACUATION TO SAFE REFUGE NICHE REQUIRED"
            tier = "TIER_3_CONTROL_ROOM"
        elif ttd_seconds <= OperationalSafetyConfig.TTD_CRITICAL_SECONDS or distance_meters <= 300:
            status = "CRITICAL"
            action = "MOVE TO DESIGNATED SAFE REFUGE ZONE IMMEDIATELY"
            tier = "TIER_1_SUPERVISOR"
        elif ttd_seconds <= OperationalSafetyConfig.TTD_WARNING_SECONDS or distance_meters <= 600:
            status = "WARNING"
            action = "PREPARE TO CLEAR TRACK & LOG ACKNOWLEDGEMENT"
            tier = "TIER_0_WORKER"
        elif ttd_seconds <= OperationalSafetyConfig.TTD_ADVISORY_SECONDS or distance_meters <= 1000:
            status = "CAUTION"
            action = "APPROACHING TRAIN ADVISORY - MONITOR TELEMETRY"
            tier = "TIER_0_WORKER"
        else:
            status = "SAFE"
            action = "MAINTAIN ROUTINE SAFETY AWARENESS"
            tier = "TIER_0_WORKER"

        return {
            "worker_id": worker_id,
            "status": status,
            "state": status,
            "distance_meters": round(distance_meters, 1),
            "ttd_seconds": ttd_seconds,
            "ttd_formatted": ttd_formatted,
            "required_action": action,
            "envelope": envelope,
            "escalation_tier": tier,
            "train_context": {
                "train_id": train_id,
                "number": train_number,
                "name": train_name,
                "speed_kmh": train_speed_kmh,
                "direction": train_direction,
                "current_block": block_section_code,
            },
        }

    @classmethod
    def evaluate_escalation_tier(
        cls,
        unacknowledged_seconds: int,
        current_tier: str,
        safety_status: str,
    ) -> str:
        """
        Determines escalation tier based on unacknowledged alert elapsed time.
        """
        if safety_status in ["CRITICAL", "EMERGENCY"]:
            if unacknowledged_seconds >= OperationalSafetyConfig.ESCALATION_CONTROL_ROOM_TIMEOUT_SEC:
                return "TIER_3_CONTROL_ROOM"
            elif unacknowledged_seconds >= OperationalSafetyConfig.ESCALATION_SUPERVISOR_TIMEOUT_SEC:
                return "TIER_1_SUPERVISOR"
        return current_tier
