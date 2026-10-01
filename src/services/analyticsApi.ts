import { apiClient } from '../api/client';

export interface OperationalKPIs {
  timestamp: string;
  active_workers: number;
  at_risk_workers: number;
  active_teams: number;
  active_trains: number;
  active_work_zones: number;
  alerts: {
    unacknowledged_total: number;
    critical: number;
    warning: number;
    escalated: number;
  };
  active_emergencies: number;
  degradations: {
    low_battery: number;
    degraded_network: number;
  };
  near_misses_total: number;
  system_status: string;
}

export interface TimelineEvent {
  id: string;
  timestamp: string;
  category: string;
  event_type: string;
  severity: string;
  summary: string;
  entity_type: string;
  entity_id: string;
  details: Record<string, any>;
}

export interface SafetyMetrics {
  timeframe: string;
  period_start: string;
  period_end: string;
  metrics: {
    total_alerts: number;
    avg_ack_time_seconds: number;
    escalation_rate_percent: number;
    near_miss_count: number;
    emergency_events_count: number;
    safety_envelope_reliability_percent: number;
  };
  severity_distribution: Record<string, number>;
}

export interface HeatmapPoint {
  id: string;
  latitude: number;
  longitude: number;
  weight: number;
  type: string;
  severity: string;
  label: string;
}

export const fetchOperationalKPIs = async (): Promise<OperationalKPIs> => {
  return apiClient<OperationalKPIs>('/analytics/kpis');
};

export const fetchEventTimeline = async (limit = 50): Promise<TimelineEvent[]> => {
  return apiClient<TimelineEvent[]>(`/analytics/timeline?limit=${limit}`);
};

export const fetchSafetyMetrics = async (timeframe = 'today'): Promise<SafetyMetrics> => {
  return apiClient<SafetyMetrics>(`/analytics/safety-metrics?timeframe=${timeframe}`);
};

export const fetchSafetyHeatmap = async (): Promise<HeatmapPoint[]> => {
  return apiClient<HeatmapPoint[]>('/analytics/heatmap');
};
