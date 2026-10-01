import { apiClient } from '../api/client';

export interface AIQueryResponse {
  query: string;
  status: string;
  answer_type: string;
  answer: string;
  disclaimer: string;
  data_sources: string[];
  timestamp: string;
}

export interface AIReportResponse {
  report_type: string;
  title: string;
  generated_at: string;
  markdown_content: string;
  disclaimer: string;
}

export interface SafetyDoc {
  id: string;
  title: string;
  category: string;
  content: string;
}

export const queryAIAssistant = async (queryText: string): Promise<AIQueryResponse> => {
  return apiClient<AIQueryResponse>('/ai/query', {
    method: 'POST',
    body: JSON.stringify({ query: queryText }),
  });
};

export const generateAIReport = async (reportType: string, timeRange = 'today'): Promise<AIReportResponse> => {
  return apiClient<AIReportResponse>('/ai/reports', {
    method: 'POST',
    body: JSON.stringify({ report_type: reportType, time_range: timeRange }),
  });
};

export const searchKnowledgeBase = async (queryText: string): Promise<SafetyDoc[]> => {
  return apiClient<SafetyDoc[]>('/ai/knowledge', {
    method: 'POST',
    body: JSON.stringify({ query: queryText }),
  });
};
