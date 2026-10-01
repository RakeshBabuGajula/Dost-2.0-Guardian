# Feature Prioritization Matrix: DOST Guardian 2.0

---

## 1. Feature Prioritization Framework

Features are classified into 4 priority tiers based on safety criticality, technical risk, and business value:
- **P0 (MVP / Safety-Critical)**: Essential for core real-time safety, fail-safe operation, and basic supervisor tracking. Non-negotiable for initial prototype release.
- **P1 (High-Value)**: Essential operational enhancements (team management, multi-tier escalation, degraded network mesh relay).
- **P2 (Advanced)**: Advanced analytical tools (near-miss heatmapping, historical playback, multi-sensor dead reckoning).
- **P3 (Future Research)**: Experimental AI features, automated environmental integration, and automated signal interlocking adapters.

---

## 2. Detailed Feature Matrix

| Feature | Target User | Business Value | Safety Value | Technical Complexity | Risk Level | Priority Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dynamic Safety Envelope** | Worker, Supervisor | High | **CRITICAL** | High | Medium | **P0 (MVP)** |
| **Deterministic Time-to-Danger (TTD)** | Worker | High | **CRITICAL** | Medium | Low | **P0 (MVP)** |
| **Multi-Level Safety Alerts (5-State)** | Worker, Supervisor | High | **CRITICAL** | Low | Low | **P0 (MVP)** |
| **Worker Acknowledgement Engine** | Worker | High | **CRITICAL** | Low | Low | **P0 (MVP)** |
| **Last-Known Safe Location (LKSL)** | Supervisor, Control Room | High | **CRITICAL** | Medium | Low | **P0 (MVP)** |
| **Basic Device & Network Health Monitor** | Admin, Supervisor | Medium | High | Low | Low | **P0 (MVP)** |
| **Railway Digital Twin Simulator** | Admin, Dev Team | **CRITICAL** | High | High | Low | **P0 (MVP)** |
| **Team Safety Accountability Matrix** | Supervisor | High | High | Medium | Low | **P1** |
| **Multi-Tier Automated Escalation** | Supervisor, Control Room | High | **CRITICAL** | Medium | Medium | **P1** |
| **Degraded Network Safety Mode (Mesh)** | Worker, Supervisor | High | High | High | High | **P1** |
| **Near-Miss Intelligence Detector** | Safety Manager, SSE | High | High | Medium | Low | **P1** |
| **Safety Heatmap & Hotspot Analysis** | Safety Manager, SSE | High | Medium | Medium | Low | **P2** |
| **Environmental Risk Layer (Weather/Visibility)** | Supervisor | Medium | Medium | Medium | Low | **P2** |
| **Post-Session Playback & Audit Timeline** | Safety Manager, Admin | Medium | Medium | Low | Low | **P2** |
| **AI Safety Trend Summarization (RAG)** | Safety Manager, Executive | Medium | Low (Analytics) | High | Low | **P2** |
| **AI Natural Language Query Assistant** | Safety Manager | Low | Low | High | Medium | **P3** |
| **Automated Signal Interlocking Adapter** | Control Room | Very High | **CRITICAL** | Extreme | High | **P3** |

---

## 3. Prioritization Rationale & Safety Boundaries

1. **Safety over AI Novelty**: Features providing direct fail-safe alerts (P0/P1) are strictly prioritized over AI analytics (P2/P3). AI is never placed on the critical alert path.
2. **Simulation Priority**: The Railway Digital Twin Simulator is classified as **P0** because it provides the synthetic test environment necessary to validate all safety rules and real-time event latency before field testing.
3. **Degraded Network Mesh**: Classified as **P1** due to high technical complexity of Bluetooth Low Energy / Wi-Fi Direct peer mesh protocol on mobile platforms.
