import { apiClient } from './client';
import { Train } from '../types/railway';

export const trainsApi = {
  getTrains: async (): Promise<Train[]> => {
    return apiClient<Train[]>('/trains');
  },
  getTrainById: async (trainId: string): Promise<Train> => {
    return apiClient<Train>(`/trains/${trainId}`);
  },
};
