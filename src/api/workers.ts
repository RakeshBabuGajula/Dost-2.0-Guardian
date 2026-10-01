import { apiClient } from './client';
import { Worker } from '../types/railway';

export const workersApi = {
  getWorkers: async (): Promise<Worker[]> => {
    return apiClient<Worker[]>('/workers');
  },
  getWorkerById: async (workerId: string): Promise<Worker> => {
    return apiClient<Worker>(`/workers/${workerId}`);
  },
};
