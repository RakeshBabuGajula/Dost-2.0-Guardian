# System Requirements Specification: DOST Guardian 2.0

---

## 1. Functional Requirements (FR)

### FR-1: Real-Time Safety Envelope & Alerting
- **FR-1.1**: The system shall compute a Dynamic Safety Envelope around each active worker based on train speed, track geometry, and configured safety buffers.
- **FR-1.2**: The system shall calculate Time-to-Danger (TTD) in seconds between an approaching train vector and a worker's active work zone.
- **FR-1.3**: The mobile app shall support 5 distinct alert states: `SAFE`, `CAUTION`, `WARNING`, `CRITICAL`, and `EMERGENCY`.
- **FR-1.4**: In `CRITICAL` state, the mobile app shall trigger a full-screen alert overlay with maximum volume siren and vibration, overriding silent mode.

### FR-2: Acknowledgement & Escalation
- **FR-2.1**: The mobile app shall provide a single-tap `[ I'M SAFE ]` button during critical alerts.
- **FR-2.2**: If a worker fails to acknowledge within $T_1 = 10\text{ seconds}$, the system shall trigger Tier-1 Supervisor Escalation.
- **FR-2.3**: If unacknowledged after $T_2 = 20\text{ seconds}$, the system shall escalate to Tier-2 Section Engineer and Tier-3 Control Room Operator.

### FR-3: Degraded Network & Offline Resilience
- **FR-3.1**: When cellular connectivity drops, the mobile app shall transition to Degraded Network Safety Mode within 6 seconds.
- **FR-3.2**: The app shall maintain a local countdown safety state using cached train trajectory vectors.
- **FR-3.3**: The app shall broadcast peer-to-peer heartbeat telemetry via Bluetooth Low Energy (BLE) / Wi-Fi Direct to nearby devices.

### FR-4: Supervisor Command Center & Monitoring
- **FR-4.1**: The supervisor web/tablet dashboard shall display a live GIS map with real-time train markers, worker markers, and dynamic safety envelopes.
- **FR-4.2**: The dashboard shall display a Team Accountability Matrix showing real-time states (`SAFE`, `WARNING`, `UNACKNOWLEDGED`, `OFFLINE`).

### FR-5: Near-Miss Intelligence & Analytics
- **FR-5.1**: The system shall automatically detect near-miss events whenever a train passes a worker location with clearance $< 3.0\text{ meters}$ or TTD at ack $< 30\text{ seconds}$.
- **FR-5.2**: The system shall generate spatial Safety Heatmaps aggregating historical near-miss locations.

---

## 2. Non-Functional Requirements (NFR)

### NFR-1: Performance & Latency
- **NFR-1.1**: End-to-end telemetry delivery latency (train position update to mobile alert display) shall be $< 300\text{ ms}$ over 4G/5G networks.
- **NFR-1.2**: The Safety Rule Engine shall process position event streams at a throughput of $\ge 5,000\text{ events/second}$ per instance.
- **NFR-1.3**: Mobile UI shall render incoming state changes at 60 fps without dropping frames during emergency alerts.

### NFR-2: Availability & Reliability
- **NFR-2.1**: High Availability (HA) architecture targeting $99.99\%$ uptime ($\le 52.5\text{ minutes}$ downtime/year).
- **NFR-2.2**: Zero single point of failure (SPOF) in core alerting pipeline. Database failover time $< 5\text{ seconds}$.

### NFR-3: Security & Privacy
- **NFR-3.1**: All API communications encrypted via TLS 1.3. Real-time WebSockets secured via TLS (`wss://`).
- **NFR-3.2**: Mobile authentication via OAuth 2.0 / JWT with strict short-lived token lifetimes (15 minutes access token, refresh token rotation).
- **NFR-3.3**: Worker location telemetry treated as sensitive operational data; encrypted at rest using AES-256.

### NFR-4: Usability & Field Accessibility
- **NFR-4.1**: 1-Second Emergency Comprehension Rule: Mobile alert screen layout must convey severity and required action within 1.0 second.
- **NFR-4.2**: Minimum touch target size on mobile emergency UI: $64 \times 64\text{ dp}$ to accommodate gloved operation.
- **NFR-4.3**: Visual contrast ratio $\ge 7:1$ for outdoor outdoor readability under direct sunlight (WCAG AAA compliant).

### NFR-5: Auditability & Compliance
- **NFR-5.1**: 100% of alert triggers, acknowledgements, escalations, and manual overrides recorded in an append-only audit log.
- **NFR-5.2**: Audit logs retained for a minimum of 7 years in immutable object storage.
