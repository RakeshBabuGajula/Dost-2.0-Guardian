# Safety Test Scenarios Specification: DOST Guardian 2.0
**Scope**: Automated Safety Validation Test Suite  

---

## 1. Safety Test Suite Matrix (15 Core Scenarios)

| Scenario ID | Test Name | Initial Condition | Trigger Event | Expected State Transition | Fail-Safe Verification Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SC-01** | Single Train Approaching Active Worker | Worker in `SAFE` state on Down Line. | Train 12626 enters block section at 110 km/h. | `SAFE` $\rightarrow$ `CAUTION` $\rightarrow$ `WARNING` $\rightarrow$ `CRITICAL` | Siren sounds within $< 300\text{ms}$ of TTD $\le 90\text{s}$ breach. |
| **SC-02** | Worker Timely Acknowledgement | Worker receiving `CRITICAL` alert ($TTD = 75\text{s}$). | Worker taps `[ I'M SAFE ]` at $t = 4\text{s}$. | `CRITICAL` $\rightarrow$ `ACKNOWLEDGED (SAFE)` | Siren immediately stops; supervisor dashboard updates to green check. |
| **SC-03** | Worker Unacknowledged (Tier-1 Escalation) | Worker receiving `CRITICAL` alert. | Worker fails to tap ACK within $T_1 = 10\text{s}$. | `CRITICAL` $\rightarrow$ `EMERGENCY (TIER-1)` | Supervisor tablet triggers high-urgency alarm with worker name/coordinates. |
| **SC-04** | Worker Unacknowledged (Tier-2/3 Escalation) | Worker in `EMERGENCY (TIER-1)`. | $T_2 = 20\text{s}$ expires without supervisor override. | `EMERGENCY (TIER-1)` $\rightarrow$ `EMERGENCY (TIER-3)` | Control room workstation sounds loud alarm; pops emergency stop prompt. |
| **SC-05** | Multiple Trains (Opposite Tracks) | Worker on Double Line section. | Train A on Up Line (80 km/h) AND Train B on Down Line (110 km/h). | System tracks both vectors; evaluates minimum TTD. | App presents alert for the most urgent train vector without race conditions. |
| **SC-06** | Worker Outside Designated Work Zone | Worker active in Session WS-1. | Worker strays $> 50\text{m}$ outside approved work polygon. | `SAFE` $\rightarrow$ `CAUTION (OFF-ZONE)` | Mobile app displays `OUTSIDE WORK ZONE` warning banner; alerts supervisor. |
| **SC-07** | Network Disconnection During Alert | Worker in `WARNING` state. | Cellular signal drops to 0 bars. | `WARNING` $\rightarrow$ `DEGRADED NETWORK SAFETY MODE` | App maintains local TTD countdown; switches banner to orange; triggers BLE mesh. |
| **SC-08** | Complete GPS Lock Loss | Worker in `ACTIVE` session. | GNSS satellite locks drop to 0 in tunnel. | Location accuracy marker changes to `UNKNOWN (±50m)`. | Safety Envelope automatically expands by $+200\text{m}$; displays uncertainty ring. |
| **SC-09** | Battery Drop to Critical Level | Worker phone at 16% battery. | Battery drops to 14%. | App enters `BATTERY_CRITICAL` mode. | App forces Dark Mode base screen; notifies supervisor tablet. |
| **SC-10** | Duplicate Telemetry Frames | Safety Engine running. | Ingestion of 5 identical `TRAIN_POSITION` packets within 10ms. | Engine processes first packet; drops remaining 4. | Bloom filter deduplication verified; state machine executed exactly once. |
| **SC-11** | Delayed Out-of-Order Telemetry | Worker position stream active. | Packet from $t = -15\text{s}$ arrives after packet from $t = 0\text{s}$. | Out-of-order packet silently discarded. | Spatial state maintained monotonically. |
| **SC-12** | Server Restart / Process Crash | Session WS-1 active. | Backend container terminated SIGKILL. | Replica container takes over WebSocket connections within 2s. | Client reconnects automatically without losing session state. |
| **SC-13** | Emergency SOS Manual Trigger | Worker in `SAFE` state. | Worker holds manual SOS button for 3 seconds. | `SAFE` $\rightarrow$ `EMERGENCY (MANUAL SOS)` | Instant broadcast to supervisor and control room regardless of train proximity. |
| **SC-14** | Near-Miss Spatial Clearance Breach | Train passes worker location. | Minimum spatial clearance measured at $1.8\text{m}$ ($< 3.0\text{m}$). | `ALERT_RESOLVED` $\rightarrow$ `NEAR_MISS_DETECTED` | Event logged in `near_misses` database table; highlighted on Safety Heatmap. |
| **SC-15** | Work Session Roll Call Closeout | Session close requested. | 1 worker device still inside active track buffer zone. | `CLOSE_DENIED` | Supervisor dashboard blocks session close until all workers clear track zone. |
