import { BackendConnectionState } from '../../types/backend';

export type WebSocketEventCallback = (type: string, payload: unknown) => void;
export type ConnectionStateCallback = (state: BackendConnectionState) => void;

export class ReconnectingWebSocketClient {
  private url: string;
  private ws: WebSocket | null = null;
  private isExplicitlyClosed = false;
  private connectionState: BackendConnectionState = 'OFFLINE';

  private reconnectAttempts = 0;
  private maxReconnectAttempts = 20;
  private baseBackoffMs = 1000;
  private maxBackoffMs = 30000;
  private reconnectTimer: number | null = null;
  private heartbeatTimer: number | null = null;

  private eventListeners: WebSocketEventCallback[] = [];
  private stateListeners: ConnectionStateCallback[] = [];

  constructor(url?: string) {
    const wsUrl = url || import.meta.env.VITE_WEBSOCKET_URL || 'ws://localhost:8000/api/v1/ws/operations';
    this.url = wsUrl;
  }

  public connect(): void {
    if (this.ws && (this.ws.readyState === WebSocket.CONNECTING || this.ws.readyState === WebSocket.OPEN)) {
      return;
    }

    this.isExplicitlyClosed = false;
    this.setConnectionState('CONNECTING');

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.reconnectAttempts = 0;
        this.setConnectionState('CONNECTED');
        this.startHeartbeat();
      };

      this.ws.onmessage = (event: MessageEvent) => {
        try {
          const msg = JSON.parse(event.data);
          this.handleIncomingMessage(msg);
        } catch {
          // Ignore parse errors
        }
      };

      this.ws.onerror = () => {
        this.setConnectionState('DEGRADED');
      };

      this.ws.onclose = () => {
        this.stopHeartbeat();
        if (!this.isExplicitlyClosed) {
          this.setConnectionState('OFFLINE');
          this.scheduleReconnect();
        }
      };
    } catch {
      this.setConnectionState('OFFLINE');
      this.scheduleReconnect();
    }
  }

  public disconnect(): void {
    this.isExplicitlyClosed = true;
    this.stopHeartbeat();
    if (this.reconnectTimer) {
      window.clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.setConnectionState('OFFLINE');
  }

  public subscribe(onEvent: WebSocketEventCallback): () => void {
    this.eventListeners.push(onEvent);
    return () => {
      this.eventListeners = this.eventListeners.filter((l) => l !== onEvent);
    };
  }

  public subscribeState(onState: ConnectionStateCallback): () => void {
    this.stateListeners.push(onState);
    onState(this.connectionState);
    return () => {
      this.stateListeners = this.stateListeners.filter((l) => l !== onState);
    };
  }

  public getConnectionState(): BackendConnectionState {
    return this.connectionState;
  }

  private setConnectionState(state: BackendConnectionState) {
    if (this.connectionState !== state) {
      this.connectionState = state;
      this.stateListeners.forEach((listener) => listener(state));
    }
  }

  private handleIncomingMessage(msg: { type: string; payload?: unknown }) {
    if (msg.type === 'HEARTBEAT') {
      return;
    }
    this.eventListeners.forEach((listener) => listener(msg.type, msg.payload));
  }

  private scheduleReconnect() {
    if (this.isExplicitlyClosed || this.reconnectAttempts >= this.maxReconnectAttempts) {
      return;
    }

    this.reconnectAttempts += 1;
    // Bounded exponential backoff with random jitter (Section 19)
    const exponentialDelay = Math.min(
      this.baseBackoffMs * Math.pow(2, this.reconnectAttempts - 1),
      this.maxBackoffMs
    );
    const jitter = Math.floor(Math.random() * 500);
    const delay = exponentialDelay + jitter;

    this.reconnectTimer = window.setTimeout(() => {
      this.connect();
    }, delay);
  }

  private startHeartbeat() {
    this.stopHeartbeat();
    this.heartbeatTimer = window.setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'PING' }));
      }
    }, 15000);
  }

  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      window.clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }
}
