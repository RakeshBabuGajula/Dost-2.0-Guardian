# System Architecture Specification: DOST Guardian 2.0

**Architecture Pattern**: Modular Monolith with Event-Driven Real-Time Gateway  

---

## 1. High-Level Architecture Overview

DOST Guardian 2.0 is designed as a highly reliable, low-latency, modular architecture. The core application logic runs as a **Modular Monolith** to maximize memory performance, simplify deployment, and eliminate inter-microservice network latency during critical alert processing. Real-time telemetry streaming is powered by WebSockets backed by Redis Streams.

```text
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|  +---------------------------+  +----------------------------------------------+  |
|  |   Worker Mobile App       |  |  Supervisor & Control Room Web Command       |  |
|  |   (Flutter / Dart)        |  |  (React / TypeScript / Tailwind CSS / Leaflet)|  |
|  +-------------+-------------+  +----------------------+-----------------------+  |
+----------------|---------------------------------------|--------------------------+
                 | REST (HTTPS) / WSS (WebSocket)        | REST (HTTPS) / WSS (WebSocket)
+----------------v---------------------------------------v--------------------------+
|                              API & EDGE GATEWAY                                   |
|  +-----------------------------------------------------------------------------+  |
|  |   Nginx Reverse Proxy / TLS 1.3 Termination / Rate Limiter                   |  |
|  +--------------------------------------+--------------------------------------+  |
+-----------------------------------------|-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
|                      MODULAR BACKEND CORE (FastAPI / Python 3.12)                 |
|                                                                                   |
|  +------------------------+  +-------------------------+  +--------------------+  |
|  |  Authentication & RBAC |  |  Work Session Manager   |  | Device Health      |  |
|  +------------------------+  +-------------------------+  +--------------------+  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |  DETERMINISTIC SAFETY RULE ENGINE (`SafetyEngine`)                          |  |
|  |  - Dynamic Safety Envelope Calculation (PostGIS / Shapely)                  |  |
|  |  - Time-to-Danger (TTD) Matrix Engine                                       |  |
|  |  - Multi-Tier Escalation Timer Manager                                      |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
|  +------------------------+  +-------------------------+  +--------------------+  |
|  |  Near-Miss Detector    |  | Safety Heatmap Engine   |  | Audit Log Service  |  |
|  +------------------------+  +-------------------------+  +--------------------+  |
+--------------------|--------------------+-------------------|---------------------+
                     |                    |                   |
+--------------------v--------------------+-------------------v---------------------+
|                             DATA & EVENT INFRASTRUCTURE                           |
|  +-----------------------+  +-----------------------+  +-----------------------+  |
|  | PostgreSQL + PostGIS  |  | Redis & Redis Streams |  | Railway Digital Twin  |  |
|  | (Geospatial Storage)  |  | (Event Bus & Cache)   |  | Simulator Engine      |  |
|  +-----------------------+  +-----------------------+  +-----------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Technology Stack Evaluation & Selection

| Layer | Chosen Technology | Rationale & Justification | Alternatives Evaluated |
| :--- | :--- | :--- | :--- |
| **Worker Mobile App** | **Flutter (Dart)** | Single cross-platform codebase; compiling to native ARM; 60fps UI performance; native BLE/GPS plugins. | React Native (JS bridge overhead), Native Kotlin/Swift (dual code cost). |
| **Supervisor Web** | **React + TypeScript** | Enterprise ecosystem; rich UI component libraries (shadcn/ui, Tailwind CSS); Leaflet/Mapbox integration. | Vue.js, Angular. |
| **Backend Framework** | **Python (FastAPI)** | High async performance (uvicorn/asyncio); native spatial geometry libraries (Shapely/PyPROJ); fast dev loop. | Node.js/Express, Go/Gin (Go evaluated for Real-Time Safety Engine phase if engine throughput demands it). |
| **Geospatial Database** | **PostgreSQL + PostGIS** | De-facto industry standard for spatial indexing (R-Tree / GiST); spatial queries (`ST_DWithin`, `ST_Distance`). | MongoDB (weaker spatial indexing), MySQL. |
| **Cache & Event Bus** | **Redis / Redis Streams** | Sub-millisecond pub/sub and event streaming; in-memory worker spatial state tracking; WebSocket session store. | RabbitMQ, Apache Kafka (over-engineered for MVP stage). |
| **Push Notifications** | **Firebase Cloud Messaging (FCM)**| High priority APNs/GCM push channel for background app wake-lock alerts. | OneSignal, Amazon SNS. |

---

## 3. Core Component Subsystems

### 3.1 Safety Engine Subsystem (`backend/app/safety/`)
- Pure deterministic, non-blocking Python module.
- Evaluates incoming train vectors against worker positions every 1,000 ms or on position push.
- Computes spatial intersection using vector projections on line strings representing railway tracks.

### 3.2 Real-Time WebSocket Gateway (`backend/app/websocket/`)
- Manages dual-way persistent connections with mobile apps and supervisor dashboards.
- Utilizes Redis Pub/Sub channels keyed by `work_session_id` and `block_section_id`.
- Automatically handles connection heartbeats (ping interval: 2s, pong timeout: 6s).

### 3.3 Railway Digital Twin Simulator (`simulator/`)
- Isolated process generating realistic train positions, speeds, track block section state changes, and worker movements.
- Emits events directly into the Redis Stream, seamlessly mocking real signaling telemetry.
