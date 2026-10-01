import { SafetyState, DynamicSafetyEnvelope } from './safety';

export interface Worker {
  id: string;
  name: string;
  role: string;
  teamId: string;
  teamName: string;
  status: SafetyState;
  batteryLevel: number;
  gpsAccuracyMeters: number;
  networkState: 'ONLINE_4G' | 'ONLINE_5G' | 'BLE_MESH' | 'OFFLINE';
  lastPingSecondsAgo: number;
  position: {
    x: number; // Simulated Track Position X (0-1000)
    y: number; // Simulated Track Offset Y
    lat: number;
    lng: number;
  };
  currentBlockSection: string;
  envelope: DynamicSafetyEnvelope;
  unacknowledgedAlertId?: string;
}

export interface Train {
  id: string;
  number: string;
  name: string;
  line: 'UP_LINE' | 'DOWN_LINE';
  speedKmh: number;
  direction: 'EASTBOUND' | 'WESTBOUND';
  positionX: number; // Simulated coordinate along track
  positionY: number;
  currentBlockSection: string;
  estimatedStoppingDistanceMeters: number;
}

export interface WorkZone {
  id: string;
  code: string;
  name: string;
  blockSectionCode: string;
  supervisorName: string;
  assignedWorkerIds: string[];
  status: 'ACTIVE' | 'PAUSED' | 'CLOSING' | 'CLOSED';
  trackSegmentRange: { startX: number; endX: number };
}

export interface BlockSection {
  code: string;
  name: string;
  division: string;
  speedLimitKmh: number;
  isOccupied: boolean;
  activeTrainId?: string;
  activeWorkZoneId?: string;
}

export interface SystemHealthMetric {
  component: 'API_GATEWAY' | 'WEBSOCKET' | 'POSTGIS_DB' | 'REDIS_STREAM' | 'SIMULATOR' | 'FCM_PUSH';
  status: 'HEALTHY' | 'DEGRADED' | 'OFFLINE';
  latencyMs: number;
  lastSyncTimestamp: string;
}
