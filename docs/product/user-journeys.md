# User Journeys Specification: DOST Guardian 2.0


---

## Journey 1: Worker Starts a Work Session

- **Actor**: Track Worker (Ramesh), Supervisor (Rajesh)
- **Preconditions**: Worker logged into mobile app; device GPS enabled; battery > 20%.
- **Trigger**: Work gang arrives at track site for scheduled maintenance.
- **Workflow Step-by-Step**:
  1. Supervisor opens mobile app and initiates a new Work Session for "Block Section KM 120/4 - 122/8".
  2. Supervisor selects active gang members (including Ramesh) and defines work zone parameters.
  3. Ramesh receives a push invitation / prompt on his phone: `Join Work Session #WS-8849?`
  4. Ramesh taps `JOIN SESSION`.
  5. Mobile app conducts a mandatory 5-point System Health Self-Test (GPS accuracy check < 10m, Battery check, Cellular signal check, Audio/Haptic vibration test, Server ping).
  6. Self-test passes $\rightarrow$ Status changes to `ACTIVE - SAFE`. Local device establishes persistent WebSocket session with backend.
  7. Map view updates to highlight active work zone boundaries in green.
- **Postconditions**: Worker is active on backend live map; position telemetry streaming every 2 seconds.

---

## Journey 2: Train Approaches the Worker's Block Section

- **Actor**: System (Train Telemetry), Worker (Ramesh), Supervisor (Rajesh)
- **Preconditions**: Ramesh in `ACTIVE - SAFE` session. Train Express 12626 enters adjacent block section at 110 km/h.
- **Trigger**: Ingress of train event into backend safety engine via signaling adapter feed.
- **Workflow Step-by-Step**:
  1. Safety Rule Engine detects train trajectory heading towards Ramesh's block section.
  2. Engine calculates Dynamic Safety Envelope buffer (e.g., 2.5 km warning threshold based on 110 km/h train speed).
  3. Distance to safety envelope reaches threshold $\rightarrow$ State transitions from `SAFE` to `CAUTION`.
  4. Ramesh's mobile phone screen turns Amber/Yellow with high contrast banner: `TRAIN IN ADJACENT SECTION | Speed: 110 km/h | ETA to Zone: 04:30`.
  5. Low-frequency single audio beep and single vibration pulse emitted.
  6. Supervisor dashboard updates Ramesh's status badge to `CAUTION`.
- **Postconditions**: Worker informed early of approaching movement; no emergency evacuation required yet.

---

## Journey 3: Worker Receives a Critical Alert

- **Actor**: System (Safety Engine), Worker (Ramesh)
- **Preconditions**: Train moves closer; calculated Time-to-Danger (TTD) drops below 90 seconds (configurable threshold).
- **Trigger**: TTD threshold breach detected by Safety Engine.
- **Workflow Step-by-Step**:
  1. Safety Engine evaluates risk state $\rightarrow$ Transitions from `WARNING` to `CRITICAL`.
  2. Backend pushes high-priority WebSocket frame + FCM wake-lock payload to Ramesh's phone.
  3. Ramesh's screen instantly flashes high-contrast bright RED with full-screen takeover:
     ```text
     CRITICAL

     TRAIN APPROACHING - DOWN LINE
     Estimated Arrival: 01:15

     MOVE TO DESIGNATED SAFE ZONE IMMEDIATELY

     [  I'M SAFE  ]
     ```
  4. Phone speaker activates max-volume multi-tone repeating siren (ignoring silent mode); phone motor activates continuous pulse vibration.
  5. Screen locks out non-safety navigation elements to focus solely on threat awareness and acknowledgement.

---

## Journey 4: Worker Acknowledges the Alert

- **Actor**: Worker (Ramesh), Supervisor (Rajesh), Backend
- **Preconditions**: Ramesh's phone in `CRITICAL` alert state. Ramesh moves off track into safe refuge area.
- **Trigger**: Ramesh taps the large prominent `[ I'M SAFE ]` button on screen.
- **Workflow Step-by-Step**:
  1. App immediately halts local siren and vibration.
  2. App reads current GPS position and compares with designated safe refuge zone geometry.
  3. Screen displays confirmation: `ACKNOWLEDGEMENT RECEIVED. Confirming safe location...`
  4. App transmits `ALERT_ACKNOWLEDGED` payload (containing timestamp, worker ID, alert ID, GPS lat/lon, accuracy) to backend.
  5. Backend updates worker state to `ACKNOWLEDGED - SAFE`.
  6. Supervisor tablet updates Ramesh's icon from Flashing Red to Solid Green checkmark `[SAFE]`.
- **Postconditions**: Alert resolved; worker safety verified; event logged in audit trail.

---

## Journey 5: Worker Does Not Acknowledge the Alert

- **Actor**: Worker (Ramesh), Supervisor (Rajesh), System Escalation Engine
- **Preconditions**: Ramesh's phone in `CRITICAL` alert state. Ramesh fails to tap `[ I'M SAFE ]` within 10 seconds (configurable T1 threshold).
- **Trigger**: Timer T1 expires on backend safety engine.
- **Workflow Step-by-Step**:
  1. Backend detects `UNACKNOWLEDGED_ALERT` for worker Ramesh (Alert ID #ALT-902).
  2. Escalation Engine triggers **Tier-1 Supervisor Escalation**.
  3. Supervisor Rajesh's tablet screen flashes high-priority RED alarm overlay with audible alert:
     `ALERT UNACKNOWLEDGED: Ramesh Kumar (Keyman) | Down Line | TTD: 00:45 | Phone Siren Active`.
  4. Supervisor uses whistle / hand signal / direct radio to order immediate evacuation of site.
  5. Supervisor inspects site; confirms Ramesh has stepped off track but dropped phone, or assists Ramesh.
  6. Supervisor taps `OVERRIDE ACKNOWLEDGE FOR RAMESH` on tablet, entering supervisor authorization PIN.
  7. Backend logs supervisor manual override with reasoning.

---

## Journey 6: Worker Loses Network Connectivity

- **Actor**: Worker (Ramesh), Mobile App (Offline Manager)
- **Preconditions**: Ramesh in `ACTIVE - SAFE` session. Worker moves into deep rock cutting; 4G network drops to 0 bars.
- **Trigger**: WebSocket heartbeats fail for 3 consecutive intervals (6 seconds).
- **Workflow Step-by-Step**:
  1. Mobile app detects network disconnect (`NETWORK_LOST`).
  2. App switches local state machine to **Degraded Network Safety Mode**.
  3. Top navigation banner turns High-Contrast Orange: `DEGRADED NETWORK - OFFLINE SAFETY ACTIVE`.
  4. App utilizes local cached train timetable / last-known train velocity vectors to maintain a local conservative safety countdown.
  5. App activates BLE (Bluetooth Low Energy) / Wi-Fi Direct peer mesh broadcaster, sending heartbeats to nearby gang members' devices.
  6. Nearby gang member's phone receives BLE mesh heartbeat and relays Ramesh's status to server when its own cellular link is restored.
  7. Backend marks Ramesh as `DEGRADED_NETWORK` on supervisor dashboard, showing last-known safe location pin with age indicator (e.g., `Offline 45s ago`).

---

## Journey 7: Worker Loses GPS

- **Actor**: Worker (Ramesh), Mobile App
- **Preconditions**: Ramesh enters thick forest canopy or tunnel; GNSS satellite locks drop below 4 satellites; location accuracy degrades from 5m to > 50m.
- **Trigger**: Mobile OS location manager emits low-accuracy telemetry event.
- **Workflow Step-by-Step**:
  1. App detects `GPS_ACCURACY_DEGRADED` (> 30 meters).
  2. App displays warning bar: `GPS LOCATION UNCERTAIN (±45m) - RE-ESTABLISHING LOCK...`
  3. Safety Engine expands Ramesh's Dynamic Safety Envelope automatically by +200 meters to compensate for spatial ambiguity.
  4. App switches to cell-tower / BLE beacon / accelerometer dead-reckoning fallback if available.
  5. Backend updates supervisor view: Ramesh's location pin expands into a shaded uncertainty circle.

---

## Journey 8: Worker's Phone Battery Becomes Critically Low

- **Actor**: Worker (Ramesh), Mobile App, Supervisor (Rajesh)
- **Preconditions**: Ramesh working 6 hours into shift; battery drops to 15%.
- **Trigger**: Battery level drops below critical threshold (15%).
- **Workflow Step-by-Step**:
  1. App triggers `BATTERY_CRITICAL` event.
  2. App switches screen to Ultra Low Power Dark Mode (disabling high-refresh animations, optimizing GPS polling intervals safely).
  3. Local alert pops up: `BATTERY AT 15% - ATTACH POWER BANK OR NOTIFY SUPERVISOR`.
  4. App sends `DEVICE_HEALTH_ALERT` telemetry packet to backend.
  5. Supervisor tablet displays yellow battery icon next to Ramesh: `Ramesh Kumar: Battery 15%`.
  6. Supervisor provides Ramesh with spare rugged battery pack or assigns paired buddy worker.

---

## Journey 9: Supervisor Monitors a Team

- **Actor**: Supervisor (Rajesh)
- **Preconditions**: Rajesh logged into Supervisor Web/Tablet Dashboard; 12 track maintainers active in field.
- **Trigger**: Continuous live operational monitoring during 4-hour track maintenance block.
- **Workflow Step-by-Step**:
  1. Rajesh views Live GIS Railway Map showing real-time position markers for all 12 workers, upcoming train vector predictions, and block section boundaries.
  2. Dashboard displays **Team Accountability Summary Bar**:
     - `10 SAFE` (Green)
     - `1 CAUTION` (Yellow)
     - `1 DEGRADED NETWORK` (Orange)
     - `0 CRITICAL / UNACKNOWLEDGED` (Red)
  3. Rajesh clicks on any worker marker to inspect real-time battery (84%), GPS accuracy (4m), network latency (42ms), and current distance to nearest rail line (6.2m).
  4. When a train enters adjacent section, dashboard highlights affected worker cluster in glowing amber ring, giving supervisor proactive situational awareness.

---

## Journey 10: Near-Miss Occurs

- **Actor**: System (Near-Miss Intelligence Engine), Worker (Ramesh), Safety Manager (Ananth)
- **Preconditions**: Train passes through block section. Worker Ramesh acknowledged alert and moved to safe zone, but was located only 1.8 meters from rail line during train passage (below standard 3.0m safe clearance buffer).
- **Trigger**: Post-passage spatial-temporal reconciliation event executed by backend.
- **Workflow Step-by-Step**:
  1. Backend correlates precise train passage time/coordinates with Ramesh's GPS trajectory log.
  2. Engine calculates minimum spatial clearance during passage: $d_{\text{min}} = 1.8\text{ meters}$.
  3. Engine classifies event as `NEAR_MISS_DETECTED` (Severity: Moderate - Spatial Clearance Breach).
  4. Incident record automatically generated with attached telemetry snippet (train speed, worker location trace, TTD at acknowledgment).
  5. System generates Near-Miss Card on Section Engineer and Safety Manager dashboards.
  6. Event aggregated into spatial Safety Heatmap for monthly engineering safety reviews.

---

## Journey 11: Emergency Escalation Occurs

- **Actor**: Worker (Ramesh), Supervisor (Rajesh), Section Engineer (Vikram), Control Room (Priya)
- **Preconditions**: Ramesh in `CRITICAL` alert state due to oncoming Express train. Ramesh unconscious on track.
- **Trigger**: T1 (10s) and T2 (20s) escalation timers expire without acknowledgement.
- **Workflow Step-by-Step**:
  1. **T0 (0s)**: Ramesh phone siren sounds. Unacknowledged.
  2. **T1 (+10s)**: Tier-1 Supervisor Escalation triggered. Rajesh's tablet alarms. Rajesh is 400m away around curve, unable to reach Ramesh immediately.
  3. **T2 (+20s)**: Unacknowledged state persists $\rightarrow$ **Tier-2 Section Engineer & Tier-3 Control Room Escalation** simultaneously triggered.
  4. Control Room Operator Priya's workstation emits high-urgency audio alarm; red flashing banner pops up over Central Traffic Controller screen:
     `EMERGENCY: UNACKNOWLEDGED WORKER ON DOWN LINE | KM 121/4 | Train #12626 approaching in 00:35`.
  5. Control Room Operator immediately verifies track location, contacts Loco Pilot via emergency radio, and sets signal to RED / caution order.
  6. Emergency incident logged with full microsecond-level audit trail.

---

## Journey 12: Work Session Closes Successfully

- **Actor**: Supervisor (Rajesh), Team Workers
- **Preconditions**: Scheduled maintenance block time completed; track cleared of all equipment.
- **Trigger**: Supervisor initiates session closeout.
- **Workflow Step-by-Step**:
  1. Supervisor taps `END WORK SESSION` on tablet dashboard.
  2. App requires mandatory **Team Roll Call Checklist**: Supervisor must verify that every worker is physically present and clear of track.
  3. App cross-references GPS locations of all connected worker devices $\rightarrow$ Confirms all devices outside track danger envelope.
  4. Each worker receives prompt: `Work Session Closing. Confirm session end?` $\rightarrow$ Ramesh taps `CONFIRM`.
  5. Backend generates **Work Session Summary Report** (Duration, total alerts issued, 100% ack rate, 0 near-misses, battery usage statistics).
  6. Session transitions to `CLOSED`. Devices revert to standby mode. Audit trail archived to immutable database storage.
