import { apiClient } from './client';
import { Alert } from '../types/safety';

export const alertsApi = {
  getAlerts: async (): Promise<Alert[]> => {
    return apiClient<Alert[]>('/alerts');
  },
  acknowledgeAlert: async (alertId: string, workerId: string, acknowledgedBy?: string): Promise<Alert> => {
    return apiClient<Alert>(`/alerts/${alertId}/acknowledge`, {
      method: 'POST',
      body: JSON.stringify({
        worker_id: workerId,
        acknowledged_by: acknowledgedBy || 'Worker',
      }),
    });
  },
  triggerEmergency: async (workerId: string, triggerType: string = 'MANUAL_SOS'): Promise<Record<string, unknown>> => {
    return apiClient<Record<string, unknown>>('/emergency-events', {
      method: 'POST',
      body: JSON.stringify({
        event_id: `evt-sos-${Date.now()}`,
        worker_id: workerId,
        trigger_type: triggerType,
      }),
    });
  },
};
