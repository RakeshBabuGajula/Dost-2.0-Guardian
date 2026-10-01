# Information Architecture & Sitemap: DOST Guardian 2.0

**Document ID**: DOC-DES-03  
**Status**: Approved Navigation & Information Architecture  

---

## 1. Worker Mobile App Sitemap

```text
Worker Mobile App
├── 0.0 Splash & System Health Pre-check
├── 1.0 Secure Authentication (Biometric / PIN / OTP)
├── 2.0 Active Work Session (Default Field View)
│   ├── 2.1 Live Safety Card (Current State: SAFE / CAUTION / WARNING / CRITICAL)
│   ├── 2.2 Time-to-Danger (TTD) Monospace Countdown
│   ├── 2.3 One-Tap Emergency Acknowledgment (`[ I'M SAFE ]`)
│   └── 2.4 Quick SOS Trigger (Hold 3 seconds)
├── 3.0 Safety Map (Minimal Outdoor GIS Vector View)
│   ├── 3.1 Worker Pin & Dynamic Safety Envelope Ring
│   ├── 3.2 Nearest Track & Safe Refuge Zone Overlay
│   └── 3.3 Approaching Train Vector (Color-Coded Arrow)
├── 4.0 Team Status (Gang Safety View)
│   └── 4.1 Gang Member List & Acknowledgment Status Badges
├── 5.0 Device Health & Connectivity Bar
│   ├── 5.1 Battery Status & Power Mode Toggle
│   ├── 5.2 GNSS Satellite Lock Quality (e.g., 9 Satellites, ±4m accuracy)
│   └── 5.3 Network Health (4G Latency / BLE Peer Mesh Count)
└── 6.0 Profile & Session History
    └── 6.1 Past Shifts & Safety Drills Log
```

---

## 2. Supervisor Field Dashboard Sitemap

```text
Supervisor Tablet / Web Dashboard
├── 1.0 Command Overview (Live Operations Dashboard)
│   ├── 1.1 Team Accountability Matrix (Safe / Warning / Critical / Offline count)
│   ├── 1.2 Active Work Sessions & Assigned Block Sections
│   └── 1.3 Escalation Alert Queue (Flashing Unacknowledged Alerts)
├── 2.0 Live Railway GIS Map
│   ├── 2.1 Layer Control (Train Vectors, Block Sections, Workers, Safe Zones)
│   ├── 2.2 Worker Cluster Inspector & Distance Telemetry
│   └── 2.3 Manual Work Zone Spatial Boundary Creator
├── 3.0 Alert & Incident Center
│   ├── 3.1 Real-Time Alert Log & Acknowledgment Timestamps
│   ├── 3.2 Supervisor Manual Override Modal
│   └── 3.3 Emergency Stoppage Request Trigger
├── 4.0 Team Management
│   ├── 4.1 Gang Roster & Device Pairing
│   └── 4.2 Pre-Shift Safety Checklist & Roll Call
└── 5.0 System Health & Audit Log
    └── 5.1 Device Battery & Connectivity Matrix
```

---

## 3. Control Room & Safety Manager Command Center Sitemap

```text
Control Room & Executive Safety Portal
├── 1.0 Live Operations Control
│   ├── 1.1 Division-Wide Train & Active Work Section Map
│   ├── 1.2 Multi-Tier Escalation Command Deck
│   └── 1.3 Signalling Block & Axle Counter Telemetry Overlay
├── 2.0 Safety Intelligence & Analytics
│   ├── 2.1 Spatial Near-Miss Heatmap (Risk Hotspot Clustering)
│   ├── 2.2 Time-to-Danger Distribution & Response Latency Charts
│   └── 2.3 AI Safety Trend Insights & Automated Incident Summaries
├── 3.0 Compliance & Audit Vault
│   ├── 3.1 Immutable Incident Audit Log (Exportable PDF/CSV)
│   └── 3.2 Safety Envelope Parameter Configuration
└── 4.0 System Administration & Security
    ├── 4.1 RBAC User & Role Management
    ├── 4.2 Device Enrollment & Security Token Revocation
    └── 4.3 Simulator & Telemetry Feed Settings
```
