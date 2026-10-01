from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.services.analytics_service import AnalyticsService

# Railway Standard Safety Procedures & Knowledge Base
RAILWAY_SAFETY_MANUAL_DOCS = [
    {
        "id": "doc-sop-001",
        "title": "Indian Railways Track Work Safety Protocol (2024)",
        "category": "SAFETY_SOP",
        "content": "All gang maintainers working on main lines must maintain a minimum safe clearance of 3.0 meters from active track rails. When a train alert is issued (TTD <= 120s), workers must immediately vacate to designated safe refuge niches (NICHE, PLATFORM, or SIDE_CLEARANCE). Mandatory flagmen and lookouts must be posted when working near curves or blind spots."
    },
    {
        "id": "doc-sop-002",
        "title": "DOST Guardian 2.0 Escalation Matrix & Degradation Rules",
        "category": "SYSTEM_SOP",
        "content": "Tier 1 Alert: Triggered when TTD <= 120s. Worker must acknowledge within 10 seconds. Tier 2 Supervisor Escalation: Triggered if alert unacknowledged after 10s or TTD <= 60s. Tier 3 Control Room Emergency: Triggered if alert unacknowledged after 20s or TTD <= 30s. Degraded Network Mode: When cellular fails, BLE peer mesh holds telemetry locally and syncs idempotently upon reconnect."
    },
    {
        "id": "doc-sop-003",
        "title": "Near-Miss Recording & Investigation Guidelines",
        "category": "INVESTIGATION_SOP",
        "content": "A Near-Miss is recorded automatically when spatial clearance between a train and worker drops below 3.0 meters without an accident occurring. Near-miss logs require mandatory review by the Sectional Safety Officer within 24 hours to investigate track geometry, lookout visibility, and alerting latency."
    }
]

class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.analytics_service = AnalyticsService(db)

    def process_operational_query(self, user_role: str, query_text: str) -> Dict[str, Any]:
        """
        Processes a natural language query over application data.
        Enforces strict RBAC and grounds all answers in empirical system data.
        NEVER makes or overrides real-time safety decisions.
        """
        # RBAC Check: Ensure user role is permitted
        allowed_roles = ["SUPERVISOR", "CONTROL_ROOM", "ADMIN", "AUDITOR", "WORKER"]
        if user_role not in allowed_roles:
            return {
                "query": query_text,
                "status": "UNAUTHORIZED",
                "answer": "Error: User role does not have authorization to perform operational AI queries.",
                "disclaimer": "AI is an analytical assistant only. Deterministic SafetyEngine is authoritative for safety states.",
                "data_sources": []
            }

        q_lower = query_text.lower()
        kpis = self.analytics_service.get_operational_kpis()
        metrics = self.analytics_service.get_safety_metrics("today")

        # 1. Alert summary queries
        if "alert" in q_lower or "critical" in q_lower or "unacknowledged" in q_lower:
            unack = kpis["alerts"]["unacknowledged_total"]
            crit = kpis["alerts"]["critical"]
            esc = kpis["alerts"]["escalated"]
            ans = f"Today there are {kpis['alerts']['unacknowledged_total']} unacknowledged alerts ({crit} critical, {esc} escalated). The overall average acknowledgement response time is {metrics['metrics']['avg_ack_time_seconds']} seconds."
            sources = ["DB Table: alerts", "Analytics API: /api/v1/analytics/kpis"]

        # 2. Near-miss queries
        elif "near miss" in q_lower or "near-miss" in q_lower or "clearance" in q_lower:
            nm_count = kpis["near_misses_total"]
            if nm_count > 0:
                ans = f"A total of {nm_count} near-miss incidents are recorded in the system. Near-miss events represent spatial clearance breaches below 3.0 meters."
            else:
                ans = "NO DATA AVAILABLE: Zero near-miss incidents recorded for the selected timeframe."
            sources = ["DB Table: near_misses", "Analytics API: /api/v1/analytics/near-misses"]

        # 3. Work zone or Team queries
        elif "zone" in q_lower or "workzone" in q_lower or "team" in q_lower or "gang" in q_lower:
            ans = f"There are currently {kpis['active_work_zones']} active work zones across {kpis['active_teams']} active maintenance teams with {kpis['active_workers']} active track workers."
            sources = ["DB Table: work_zones", "DB Table: teams", "DB Table: workers"]

        # 4. Degradation / Network / Battery queries
        elif "battery" in q_lower or "network" in q_lower or "gps" in q_lower or "mesh" in q_lower:
            low_b = kpis["degradations"]["low_battery"]
            deg_net = kpis["degradations"]["degraded_network"]
            ans = f"Telemetry audit shows {low_b} workers with low battery (<20%) and {deg_net} workers operating in degraded/BLE mesh network mode."
            sources = ["DB Table: workers", "DB Table: devices"]

        # 5. Default operational overview
        else:
            ans = f"System Operational Summary: {kpis['active_workers']} active workers, {kpis['active_trains']} trains tracked, {kpis['active_work_zones']} active work zones, {kpis['alerts']['unacknowledged_total']} active alerts, and {kpis['near_misses_total']} near misses recorded."
            sources = ["Operational Command Analytics Engine"]

        return {
            "query": query_text,
            "status": "SUCCESS",
            "answer_type": "AI-GENERATED ANALYSIS",
            "answer": ans,
            "disclaimer": "AI IS AN ANALYTICAL ASSISTANT ONLY. Safety-critical decisions are governed exclusively by the deterministic SafetyEngine.",
            "data_sources": sources,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def generate_operational_report(self, user_role: str, report_type: str, time_range: str = "today") -> Dict[str, Any]:
        """Generates structured operational reports based on empirical database telemetry."""
        kpis = self.analytics_service.get_operational_kpis()
        metrics = self.analytics_service.get_safety_metrics(time_range)

        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        title = f"DOST GUARDIAN 2.0 — {report_type.replace('_', ' ')} ({time_range.upper()})"
        
        content = f"""# {title}
**Generated At:** {now_str}
**Role:** {user_role}
**System Status:** {kpis['system_status']}

---

### EXECUTIVE SUMMARY
This operational safety report summarizes system telemetry, worker exposure, and real-time safety envelope metrics. All metrics are grounded in recorded database events.

### FACTUAL OPERATIONAL METRICS
- **Active Track Workers:** {kpis['active_workers']}
- **Active Maintenance Teams:** {kpis['active_teams']}
- **Active Trains Tracked:** {kpis['active_trains']}
- **Active Work Zones:** {kpis['active_work_zones']}
- **Total Alerts Created:** {metrics['metrics']['total_alerts']}
- **Average Acknowledgement Latency:** {metrics['metrics']['avg_ack_time_seconds']}s (Target: < 10.0s)
- **Escalation Rate:** {metrics['metrics']['escalation_rate_percent']}%
- **Recorded Near-Misses:** {metrics['metrics']['near_miss_count']}
- **Active Emergencies / SOS:** {kpis['active_emergencies']}

### TELEMETRY & DEGRADATION AUDIT
- **Low Battery Devices (<20%):** {kpis['degradations']['low_battery']}
- **Degraded Network / BLE Mesh Workers:** {kpis['degradations']['degraded_network']}

### ALERT SEVERITY DISTRIBUTION
- **SAFE / ADVISORY:** {metrics['severity_distribution']['SAFE']}
- **CAUTION:** {metrics['severity_distribution']['CAUTION']}
- **WARNING:** {metrics['severity_distribution']['WARNING']}
- **CRITICAL:** {metrics['severity_distribution']['CRITICAL']}
- **EMERGENCY:** {metrics['severity_distribution']['EMERGENCY']}

---
> [!NOTE]
> **DISCLAIMER**: This report is an AI-assisted operational summary. Deterministic rule-based evaluation by the SafetyEngine governs real-time safety state transitions.
"""

        return {
            "report_type": report_type,
            "title": title,
            "generated_at": now_str,
            "markdown_content": content,
            "disclaimer": "AI-ASSISTED SUMMARY — FOR OPERATIONAL REVIEW ONLY"
        }

    def search_knowledge_base(self, query_text: str) -> List[Dict[str, Any]]:
        """Searches railway standard operating procedures and documentation."""
        q_lower = query_text.lower()
        results = []

        for doc in RAILWAY_SAFETY_MANUAL_DOCS:
            if any(term in doc["title"].lower() or term in doc["content"].lower() for term in q_lower.split()):
                results.append(doc)

        if not results:
            return RAILWAY_SAFETY_MANUAL_DOCS  # Return full docs if broad query

        return results
