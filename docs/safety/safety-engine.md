# Safety Rule Engine Specification: DOST Guardian 2.0

**Module Name**: `backend.app.safety.SafetyEngine`  
**Engine Type**: Pure Deterministic State Machine  

---

## 1. Safety Engine Conceptual Pipeline

The Safety Engine is the core deterministic calculator of DOST Guardian 2.0. It receives high-frequency train telemetry and worker location streams, calculates spatial clearances against track geometries, determines Time-to-Danger (TTD), and triggers state machine transitions.

```text
[ Train Telemetry Stream ] + [ Worker Location Telemetry ] + [ Track Block Geometry ]
                                        |
                                        v
                    +---------------------------------------+
                    | Dynamic Safety Envelope Calculator    |
                    | (PostGIS Spatial Buffer Projection)   |
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    | Time-to-Danger (TTD) Matrix Engine    |
                    | TTD = Distance / Train Velocity       |
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    | Deterministic State Machine Transition|
                    | SAFE -> CAUTION -> WARNING -> CRITICAL|
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    | Alert Dispatch & Escalation Manager   |
                    | (WebSocket / FCM / Timer T1/T2/T3)    |
                    +---------------------------------------+
```

---

## 2. Dynamic Safety Envelope Calculation Model

The Dynamic Safety Envelope around a worker or work gang is calculated dynamically to ensure adequate warning time regardless of train speed or track geometry.

### Mathematical Formulation
$$\text{Buffer Distance } (D_{\text{buffer}}) = D_{\text{reaction}} + D_{\text{clearance}} + D_{\text{stopping}}$$

Where:
- $D_{\text{reaction}} = v_{\text{train}} \times t_{\text{reaction}}$ (where $t_{\text{reaction}} = 10.0\text{ seconds}$ worker perception & evacuation buffer)
- $D_{\text{clearance}} = 3.0\text{ meters}$ minimum physical track clearance line
- $D_{\text{uncertainty}} = \text{GPS Accuracy Buffer}$ (e.g., $+15\text{m}$ if accuracy $> 10\text{m}$)
- $v_{\text{train}} = \text{Current reported train ground speed in m/s}$

### Dynamic Envelope Radius Example Table

| Train Speed ($v_{\text{train}}$) | Reaction Time ($t_{\text{reaction}}$) | Base Spatial Warning Buffer ($D_{\text{buffer}}$) | Target TTD Threshold |
| :--- | :--- | :--- | :--- |
| **30 km/h** ($8.33\text{ m/s}$) | $10\text{ s}$ | **$250\text{ meters}$** | $30\text{ seconds}$ |
| **60 km/h** ($16.67\text{ m/s}$) | $10\text{ s}$ | **$600\text{ meters}$** | $45\text{ seconds}$ |
| **110 km/h** ($30.56\text{ m/s}$) | $10\text{ s}$ | **$1,500\text{ meters}$** | $90\text{ seconds}$ |
| **160 km/h** ($44.44\text{ m/s}$) | $10\text{ s}$ | **$2,500\text{ meters}$** | $120\text{ seconds}$ |

*Note: All thresholds are explicitly marked as `CONFIGURABLE / SIMULATION VALUE` in software configuration files.*

---

## 3. State Machine Transition Logic

```text
               +-------------------------------------------------+
               |                                                 |
               v                                                 |
           +-------+       TTD <= 300s       +---------+         |
           | SAFE  | ----------------------> | CAUTION |         |
           +-------+                         +----+----+         |
               ^                                  |              |
               |                                  | TTD <= 180s  |
               | Alert Resolved / Track Cleared   v              |
               |                             +---------+         |
               +---------------------------- | WARNING |         |
               |                             +----+----+         |
               |                                  |              |
               |                                  | TTD <= 90s   |
               |                                  v              |
               |                             +----------+        |
               +---------------------------- | CRITICAL |        |
               |                             +----+-----+        |
               |                                  |              |
               |                                  | T1 Unack     |
               |                                  v              |
               |                             +-----------+       |
               +---------------------------- | EMERGENCY | -----+
                                             +-----------+
```

### State Machine Transition Rules Table

| Current State | Condition / Trigger | New State | Visual Indicator | Acoustic Indicator | Required Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SAFE** | Train enters adjacent sector ($\text{TTD} \le 300\text{s}$) | **CAUTION** | Amber Banner | Single Soft Beep | Worker maintains awareness. |
| **CAUTION** | Train enters work section ($\text{TTD} \le 180\text{s}$) | **WARNING** | Orange Flash | Double Chime | Worker prepares to clear track. |
| **WARNING** | Distance breaches envelope ($\text{TTD} \le 90\text{s}$) | **CRITICAL** | Full Red Takeover | Continuous Siren (85dB) | **IMMEDIATE EVACUATION** to safe zone. |
| **CRITICAL** | Worker taps `[ I'M SAFE ]` button | **ACKNOWLEDGED (SAFE)** | Solid Green Check | Audio Silence | Worker stays in safe refuge zone until clear. |
| **CRITICAL** | $T_1 = 10\text{s}$ timer expires without ack | **EMERGENCY (TIER-1)**| Flashing Crimson Overlay | Max Alarm + Tablet Alert | Supervisor informed; manual override triggered. |
| **EMERGENCY** | $T_2 = 20\text{s}$ timer expires without ack | **EMERGENCY (TIER-2/3)**| Flashing Crimson Overlay | Control Room Alarm | Control room issues signal stop / caution order. |
