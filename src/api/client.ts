const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    request_id?: string;
    details?: Record<string, unknown>;
  };
}

export class ApiClientError extends Error {
  public code: string;
  public status: number;
  public requestId?: string;

  constructor(message: string, code: string = 'API_ERROR', status: number = 500, requestId?: string) {
    super(message);
    this.name = 'ApiClientError';
    this.code = code;
    this.status = status;
    this.requestId = requestId;
  }
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}/api/v1${endpoint}`;
  
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  
  // Inject correlation request ID
  if (!headers.has('X-Request-ID')) {
    headers.set('X-Request-ID', `req-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorData: ApiErrorResponse | null = null;
      try {
        errorData = await response.json();
      } catch {
        // Ignore json parse error for non-json responses
      }

      const code = errorData?.error?.code || `HTTP_${response.status}`;
      const message = errorData?.error?.message || response.statusText || 'API request failed';
      const reqId = errorData?.error?.request_id || headers.get('X-Request-ID') || undefined;

      throw new ApiClientError(message, code, response.status, reqId);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (err: unknown) {
    clearTimeout(timeoutId);
    if (err instanceof ApiClientError) {
      throw err;
    }
    if (err instanceof Error && err.name === 'AbortError') {
      throw new ApiClientError('Request timeout after 10 seconds', 'TIMEOUT', 408);
    }
    throw new ApiClientError(
      err instanceof Error ? err.message : 'Network error or backend offline',
      'NETWORK_ERROR',
      0
    );
  }
}
