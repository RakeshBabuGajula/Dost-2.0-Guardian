export type SafetyState = 
  | 'SAFE'
  | 'CAUTION'
  | 'WARNING'
  | 'CRITICAL'
  | 'EMERGENCY'
  | 'DEGRADED_NETWORK'
  | 'UNKNOWN';

export type EscalationTier = 'NONE' | 'WORKER_ACK' | 'TIER_1_SUPERVISOR' | 'TIER_2_SECTION_ENG' | 'TIER_3_CONTROL_ROOM';

export interface DynamicSafetyEnvelope {
  radiusMeters: number;
  reactionTimeSeconds: number;
  clearanceBufferMeters: number;
  gpsUncertaintyBufferMeters: number;
  isExpandedDueToGps: boolean;
}

export interface Alert {
  id: string;
  workerId: string;
  workerName: string;
  trainId: string;
  trainName: string;
  blockSectionCode: string;
  state: SafetyState;
  timeToDangerSeconds: number;
  distanceToTrainMeters: number;
  escalationTier: EscalationTier;
  createdAt: string;
  acknowledgedAt?: string;
  acknowledgedBy?: string;
  isAcknowledged: boolean;
  requiredAction: string;
}

export interface NearMissEvent {
  id: string;
  occurredAt: string;
  trainId: string;
  trainSpeedKmh: number;
  workerId: string;
  workerName: string;
  blockSectionCode: string;
  minSpatialClearanceMeters: number;
  ttdAtAckSeconds: number;
  severity: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  contributingFactors: string[];
  locationCoords: { x: number; y: number };
}
