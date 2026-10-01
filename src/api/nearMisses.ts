import { apiClient } from './client';
import { NearMissEvent } from '../types/safety';

export const nearMissesApi = {
  getNearMisses: async (): Promise<NearMissEvent[]> => {
    return apiClient<NearMissEvent[]>('/near-misses');
  },
};
