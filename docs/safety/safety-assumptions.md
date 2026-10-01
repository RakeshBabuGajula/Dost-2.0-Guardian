# Safety Assumptions & Configurable Parameters: DOST Guardian 2.0


---

## 1. Grounding & Parameter Disclaimer

> [!IMPORTANT]
> **SIMULATION & PROTO-RULE DISCLAIMER**: DOST Guardian 2.0 is an engineering prototype platform. Exact real-world railway safety distances, stopping distances, and warning time thresholds vary by railway administration (e.g., Indian Railways General & Subsidiary Rules - G&SR), track speed rating, and rolling stock type.
> 
> All numeric values defined herein are marked as `CONFIGURABLE / SIMULATION VALUE / REQUIRES RAILWAY AUTHORIZATION` and MUST be validated by certified railway safety authorities prior to field deployment.

---

## 2. Configurable Parameter Registry

```json
{
  "safetyEngineConfig": {
    "version": "2.0.0-stage0",
    "disclaimer": "SIMULATION VALUES - REQUIRES RAILWAY AUTHORIZATION",
    "thresholds": {
      "timeToDanger": {
        "cautionSeconds": 300,
        "warningSeconds": 180,
        "criticalSeconds": 90,
        "emergencyEscalationT1Seconds": 10,
        "emergencyEscalationT2Seconds": 20,
        "emergencyEscalationT3Seconds": 30
      },
      "spatialClearance": {
        "minimumTrackClearanceMeters": 3.0,
        "nearMissSpatialThresholdMeters": 3.0,
        "nearMissTTDThresholdSeconds": 30,
        "defaultGpsUncertaintyBufferMeters": 15.0
      },
      "workerEvacuation": {
        "assumedEvacuationSpeedMps": 1.2,
        "perceptionReactionBufferSeconds": 10.0
      },
      "telemetryTiming": {
        "workerGpsPollingIntervalMs": 2000,
        "websocketHeartbeatIntervalMs": 2000,
        "websocketHeartbeatTimeoutMs": 6000
      }
    }
  }
}
```

---

## 3. Explicit Safety Assumptions

1. **Non-Interlocked Architecture**: DOST Guardian 2.0 operates as an independent advisory worker protection platform. It does NOT interface directly with safety-critical vital interlocking computers (e.g., EI / Relay Interlocking) to clear or throw signals in initial prototype development phases.
2. **Worker Equipment Responsibility**: Workers are assumed to carry registered, operational devices with functional speakers, vibration motors, and minimum 20% battery charge at session start.
3. **Safe Refuge Zone Pre-Definition**: Every work session requires the supervisor to pre-designate physical safe refuge zones (e.g., cess area, refuge niche in tunnel) prior to line entry.
