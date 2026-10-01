import { apiClient } from './client';
import { WorkZone } from '../types/railway';

export const workZonesApi = {
  getWorkZones: async (): Promise<WorkZone[]> => {
    return apiClient<WorkZone[]>('/work-zones');
  },
};
