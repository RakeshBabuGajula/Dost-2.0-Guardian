# Failure Analysis & Resilience Matrix: DOST Guardian 2.0

**Design Principle**: *Fail-Safe First Engineering*  

---

## 1. Resilience & Risk Mitigation Matrix

> [!NOTE]
> All target metrics (latency, recovery times, uptime) represent `[PROPOSED ENGINEERING TARGET]` benchmarks for system evaluation.

| Failure Scenario | Affected System | Risk Level | Detection Mechanism | Automated Fallback / Fail-Safe Behavior | Target Recovery Protocol `[PROPOSED ENGINEERING TARGET]` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Complete Loss of Cellular Network** | Mobile Worker App | **CRITICAL** | WebSocket heartbeat timeout (6s). | App transitions to **Degraded Network Safety Mode**; banner turns high-contrast orange; activates local countdown using cached vector; enables BLE peer mesh relay. | Auto-reconnects WebSocket on signal recovery; syncs missed telemetry buffered in SQLite. |
| **GPS Accuracy Degradation (> 30m)** | Mobile Worker App | **HIGH** | Location Manager accuracy callback $> 30\text{m}$. | Safety Engine automatically expands Dynamic Safety Envelope buffer by $+200\text{m}$; displays location uncertainty visual ring. | Reverts envelope size when satellite lock accuracy improves below $10\text{m}$. |
| **Backend Server Process Crash** | Real-Time Engine | **CRITICAL** | Systemd / Docker healthcheck probe failure. | Nginx gateway routes traffic to standby replica instance; Redis Stream retains unacknowledged event queue without data loss. | Auto-restart by Docker container orchestrator targeting $< 2\text{ seconds}$. |
| **PostgreSQL Database Node Failover** | Data Storage | **HIGH** | Connection pool health probe failure. | Backend switches read/write queries to hot-standby PostgreSQL read-replica promoted to primary. | Automatic failover managed by Patroni / PgBouncer targeting $< 5\text{ seconds}$. |
| **Redis Cache / PubSub Failure** | Event Bus | **CRITICAL** | Connection refusal on Redis socket. | Backend falls back to local in-memory event bus queue; logs warning metrics; suspends non-essential analytics streams. | Redis Sentinel automatically promotes standby node targeting $< 3\text{ seconds}$. |
| **FCM Push Notification Service Down** | Mobile Alerts | **HIGH** | FCM HTTP API 503 / Timeout response. | System relies on active persistent WebSocket connection as primary alert channel; triggers SMS backup gateway for Tier-2 escalations. | Re-establishes FCM push token registration upon service recovery. |
| **Worker Phone Battery Below 5%** | Worker Device | **HIGH** | Battery Manager broadcast OS event. | App triggers high-priority sound alarm; sends `BATTERY_CRITICAL` event to supervisor; locks UI to dark mode base telemetry state. | Supervisor pairs worker with buddy or replaces battery pack. |
| **Duplicate Event Ingestion** | Safety Engine | **MEDIUM** | Authoritative Redis `SET NX` key lock + DB constraint check (optional preliminary Bloom filter). | Duplicate event is silently dropped without re-executing state machine or triggering duplicate alert audio. | Normal execution continues. |
| **Out-of-Order Position Telemetry** | Safety Engine | **MEDIUM** | Monotonic timestamp check ($t_{\text{new}} < t_{\text{last}}$). | Out-of-order stale position packet is discarded; engine retains last valid spatial coordinate state. | Normal execution continues. |
| **Device Clock Drift (> 5 seconds)** | Mobile Worker App | **MEDIUM** | NTP time synchronization audit on app startup. | Mobile app computes server-client time delta offset; adjusts local timestamp calculations to match backend server clock. | Syncs NTP time via background worker. |

---

## 2. Fail-Safe Architectural Guarantees

1. **Conservative Default**: If the exact location or train vector cannot be verified with certainty due to network or sensor failure, the system MUST default to the higher-risk state (e.g., treating `CAUTION` as `WARNING`, expanding safety buffer).
2. **Local Autonomy**: The mobile worker application MUST be capable of alerting the worker based on local cached schedule data and BLE gang heartbeats even if completely severed from the cloud server.
3. **No Silent Failures**: Any system component entering a degraded state MUST visibly broadcast its state to both the local worker UI and the supervisor command dashboard.
