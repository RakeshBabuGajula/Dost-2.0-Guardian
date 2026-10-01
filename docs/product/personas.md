# User Personas Specification: DOST Guardian 2.0

---

## Persona 1: Railway Track Worker (Field Maintenance)

- **Name**: Ramesh Kumar ("Keyman / Track Maintainer Grade I")
- **Role**: Performs physical track inspections, rail joint tightening, ballast packing, and track welding on active lines.
- **Environment**: High noise (heavy machinery, passing trains), extreme weather (bright sunlight, heavy rain), wearing thick gloves, safety helmet, high-vis jacket.

### Key Characteristics & Constraints
- **Device Used**: Ruggedized Android smartphone (IP68, high-brightness outdoor screen, physical emergency button).
- **Responsibilities**: Inspecting 5–8 km of track daily; clearing track upon train alert; acknowledging safety alerts.
- **Goals**: Stay safe while completing maintenance work on schedule; know exactly when and where a train is coming.
- **Pain Points**: Hard to see phone screen in bright sun; hard to tap small buttons while wearing gloves; ambient noise drowns out phone speakers; blind curves on multi-track lines.
- **Safety-Critical Actions**:
  1. Acknowledge CRITICAL approaching train alert within 10 seconds.
  2. Evacuate track to designated safe refuge zone upon alert.
  3. Trigger SOS manually if injured or stuck on track.
- **Permissions**: View active work session, receive alerts, acknowledge alerts, send SOS, view personal device health.
- **Failure Scenarios**: Loss of GPS signal in cutting; loss of cellular network; battery dies mid-shift; phone dropped on track.

---

## Persona 2: Work Team Supervisor

- **Name**: Rajesh Sharma ("Mate / Junior Engineer Track")
- **Role**: Leads a gang of 8–15 track maintainers working on a designated block section. Responsible for site safety and work execution.
- **Environment**: On-site with track gang, moving along track section with field tablet or smartphone.

### Key Characteristics & Constraints
- **Device Used**: High-brightness 10-inch rugged Android tablet / smartphone.
- **Responsibilities**: Authorizing work session start/stop; setting up work zone boundaries; monitoring gang acknowledgment state; conducting pre-shift safety brief.
- **Goals**: Zero accidents in team; real-time visibility of every gang member’s safety status and location; instant alert if any worker fails to respond.
- **Pain Points**: Managing multiple workers spread across 500 meters of track; maintaining phone connectivity; tracking workers who wander outside approved work zone.
- **Safety-Critical Actions**:
  1. Define and activate Work Zone boundary on mobile dashboard.
  2. Receive immediate escalation if worker fails to acknowledge CRITICAL alert within 10 seconds.
  3. Verify team safe location before clearing block section.
- **Permissions**: Create/manage work sessions, view team member locations, view team acknowledgment state, override/acknowledge team alerts in emergency, declare team safe.
- **Failure Scenarios**: Supervisor tablet drops offline; multiple workers in warning state simultaneously; worker strays off-zone.

---

## Persona 3: Section Engineer

- **Name**: Vikram Singh ("Senior Section Engineer - SSE Track")
- **Role**: Oversees track maintenance across a 50 km railway section. Manages multiple work gangs, schedules line blocks, and audits safety compliance.
- **Environment**: Office / Field inspection vehicle with laptop and tablet.

### Key Characteristics & Constraints
- **Device Used**: Laptop (Web Dashboard) and tablet.
- **Responsibilities**: Approving planned work sessions; reviewing near-miss analytics; investigating safety incidents; ensuring device health and compliance.
- **Goals**: Maximize track maintenance efficiency while strictly adhering to safety windows; reduce near-miss occurrences across section.
- **Pain Points**: Lack of historical near-miss data; reliance on paper logs for safety audits; delayed incident reporting.
- **Safety-Critical Actions**:
  1. Audit high-risk work sections and approve dynamic safety envelope configurations.
  2. Receive Tier-2 escalation if supervisor and worker fail to respond to critical emergency.
  3. Authorize emergency track stoppage requests in coordination with control room.
- **Permissions**: View all section work zones, manage section teams, access near-miss heatmaps, configure section safety parameters, generate audit reports.
- **Failure Scenarios**: Communication gap with control room during emergency block cancellation.

---

## Persona 4: Railway Control Room Operator

- **Name**: Priya Nair ("Section Controller / Chief Controller")
- **Role**: Controls train traffic, signals, and line blocks across an entire railway division from a central command center.
- **Environment**: High-density control room with multiple multi-monitor displays, video walls, and heavy radio communications.

### Key Characteristics & Constraints
- **Device Used**: Multi-monitor desktop workstation (Supervisor Web Command Center).
- **Responsibilities**: Monitoring live train positions, block section occupations, and active track worker gangs; issuing line blocks.
- **Goals**: Ensure smooth train movement without compromising track worker safety; instant awareness of worker emergency on active line.
- **Pain Points**: Visual clutter on legacy CTC screens; delayed information on worker exact coordinates vs signal track circuits.
- **Safety-Critical Actions**:
  1. Monitor active work zones overlaying live train movements.
  2. Receive Tier-3 top-level emergency escalation if worker is in critical path unacknowledged.
  3. Issue emergency stop signal / caution order to loco pilot if worker is trapped on line.
- **Permissions**: High-level live operations view, system-wide alert override, direct emergency escalation broadcast, line block status verification.
- **Failure Scenarios**: Signal feed telemetry lag; conflicting train schedule updates.

---

## Persona 5: Railway Safety Manager

- **Name**: Ananthakrishnan M. ("Divisional Safety Officer - DSO")
- **Role**: Responsible for division-wide safety policy, accident prevention, compliance auditing, and safety training.
- **Environment**: Divisional headquarters office / safety audit field visits.

### Key Characteristics & Constraints
- **Device Used**: Web Dashboard on workstation/laptop.
- **Responsibilities**: Analyzing systemic safety trends, identifying high-risk geographic clusters (hotspots), reviewing AI-generated safety summaries, conducting safety audits.
- **Goals**: Proactively eliminate safety hazards before accidents occur; enforce safety compliance protocols across all sections.
- **Pain Points**: Reactive safety management based only on actual accidents rather than near-misses; difficulty parsing raw telemetry data into actionable policy.
- **Safety-Critical Actions**:
  1. Review monthly near-miss heatmaps and audit recurring danger patterns.
  2. Enforce updated safety envelope thresholds for high-speed corridors.
  3. Export audit-compliant incident reports for railway board reviews.
- **Permissions**: Read-only global operations access, full access to analytics, heatmaps, AI reports, audit logs, and risk parameter management.

---

## Persona 6: System Administrator

- **Name**: David Chen ("Lead DevOps & Security Engineer")
- **Role**: Manages system availability, user provisioning, security RBAC, device enrollment, and server health.
- **Environment**: Operations center / Cloud management console.

### Key Characteristics & Constraints
- **Device Used**: Workstation with CLI and Admin Dashboard.
- **Responsibilities**: Maintaining system uptime (99.99%); managing JWT token lifecycles, API gateways, database backups, and simulator feeds.
- **Goals**: High platform reliability, low latency, robust security posture, zero credential leaks.
- **Pain Points**: Managing hardware/software health across thousands of mobile endpoints; detecting degraded network nodes.
- **Safety-Critical Actions**:
  1. Provision and revoke device access tokens immediately upon lost/stolen hardware reports.
  2. Monitor real-time WebSocket connection density and server queue backpressure.
  3. Execute failover procedures if primary geospatial database node degrades.
- **Permissions**: Full administrative access, system configuration, user/role management, security log access.
