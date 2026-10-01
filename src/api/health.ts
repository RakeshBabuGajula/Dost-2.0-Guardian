import { apiClient } from './client';

export interface HealthCheckResponse {
  status: 'HEALTHY' | 'DEGRADED' | 'DOWN';
  app_alive: boolean;
  db_connected: boolean;
  redis_connected: boolean;
  timestamp: string;
}

export const healthApi = {
  checkReadiness: async (): Promise<HealthCheckResponse> => {
    return apiClient<HealthCheckResponse>('/health/ready');
  },
  checkLiveness: async (): Promise<{ status: string }> => {
    return apiClient<{ status: string }>('/health/live');
  },
};
