# Product Vision & Strategy: DOST Guardian 2.0

**Product Name**: DOST Guardian 2.0  
**Tagline**: *From Train Warning to Predictive Worker Safety*  

---

## 1. Executive Product Vision

### Vision Statement
To eliminate preventable trackside railway fatalities worldwide by transforming reactive train warnings into an intelligent, multi-layered, predictive worker safety ecosystem.

### Mission Statement
To empower track workers, gang supervisors, section engineers, and railway control room operators with real-time dynamic safety envelopes, deterministic time-to-danger warnings, team accountability workflows, and fail-safe offline protection.

---

## 2. Problem Statement

Track maintainers ("Keymen", "Gangmen", and Track Maintainers) work in high-risk environments with heavy machinery, high-speed rail traffic, multi-track curves, and harsh weather conditions. Traditional track safety relies heavily on manual lookouts, hand flags, and basic block-section alerts.

### Key Operational Challenges & Failures:
1. **Late Awareness on Multi-Track Curve Sections**: Workers cannot see or hear trains approaching around blind curves or behind noise barriers until seconds before arrival.
2. **Ambiguous Urgency**: Static "block occupied" alerts tell a worker *that* a train is in the 5 km section, but fail to convey *when* it will reach their specific location.
3. **Unconscious / Incapacitated Worker Risk**: Existing apps sound an alarm on the worker's phone, but if the worker fails to respond, no higher-level escalation occurs.
4. **Network Blindspots**: Field teams working in deep cuttings or remote rural stretches frequently lose 4G connectivity, leaving cloud-reliant alert apps useless.
5. **No Systemic Safety Intelligence**: Near-misses are rarely logged or systematically analyzed, missing critical opportunities to fix high-risk work procedures before a fatality occurs.

---

## 3. Core Value Proposition & Differentiators

| Capability | Legacy Train Warning Apps | DOST Guardian 2.0 Platform |
| :--- | :--- | :--- |
| **Spatial Boundary** | Static Block Section level warning | **Dynamic Safety Envelope**: Spatial buffer computed dynamically from train speed, track geometry, and work group spread. |
| **Urgency Indicator** | Static Yellow/Red binary alert | **Time-to-Danger (TTD)**: Human-readable countdown (e.g., `02:14 to arrival`) based on real-time train movement. |
| **Team Accountability** | Single-user phone alert | **Gang Safety Matrix**: Supervisors see real-time safe/warning/unacknowledged states across all gang members. |
| **Escalation Protocol** | None (Local phone loop) | **Multi-Tier Automated Escalation**: Worker $\rightarrow$ Gang Supervisor $\rightarrow$ Section Engineer $\rightarrow$ Control Room. |
| **Network Resilience** | System down on internet loss | **Degraded Network Safety Mode**: Local peer mesh relay + last-known safe location tracking. |
| **Safety Analytics** | Basic operational logs | **Near-Miss Intelligence & Heatmaps**: Automated near-miss detection, spatial risk heatmaps, and AI trend summarization. |

---

## 4. Product Goals & Non-Goals

### Product Goals (In-Scope for Platform Design):
1. **Zero-Delay Threat Comprehension**: Enable field track workers to grasp threat severity and required action within **1 second** of screen illumination.
2. **Deterministic Safety Rules**: Guarantee sub-second alert generation (< 500 ms) via a mathematical safety rule engine.
3. **Multi-Role Synchronization**: Seamless real-time sync across mobile worker devices, supervisor field tablets, and web command centers.
4. **Fail-Safe Offline Autonomy**: Maintain local safety countdowns even during complete loss of cellular networks.
5. **Predictive Analytics & Near-Miss Heatmapping**: Capture 100% of spatial near-miss events for safety engineering audits.

### Non-Goals (Strictly Out-of-Scope):
1. **Direct Signal Interlocking Control**: DOST Guardian 2.0 will NOT directly actuate signals or trigger automatic train stopping (ATS/ETCS/Kavach) in initial prototype development phases; it functions as an independent, non-interlocked worker safety platform.
2. **Autonomous Safety Decisions by AI**: AI will NOT calculate safety envelopes or trigger evacuation alerts. Safety rules are strictly deterministic.
3. **Generic HR / Payroll Tracking**: The platform is built exclusively for track safety and operational risk, not general workforce time-tracking.

---

## 5. Strategic Success Metrics (KPIs)

1. **Alert Processing Latency**: $< 300\text{ ms}$ from train telemetry update to mobile alert delivery.
2. **1-Second Comprehension Rate**: $> 98\%$ of workers execute safe movement within 5 seconds of alert trigger during drills.
3. **Escalation Reliability**: $100\%$ of unacknowledged critical alerts escalated to supervisor within 15 seconds.
4. **Offline Safety Retention**: Zero safety gap during temporary network dropouts up to 10 minutes.
5. **Near-Miss Capture Rate**: $100\%$ spatial near-miss logging for post-shift safety analysis.
