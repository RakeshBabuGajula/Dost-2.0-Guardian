import { Worker, Train, WorkZone, BlockSection, SystemHealthMetric } from '../types/railway';
import { Alert, NearMissEvent } from '../types/safety';

export const INITIAL_WORKERS: Worker[] = [
  {
    id: 'WRK-101',
    name: 'Ramesh Kumar',
    role: 'Keyman / Track Maintainer I',
    teamId: 'TEAM-ALPHA',
    teamName: 'Gang 04 - Chennai Division',
    status: 'SAFE',
    batteryLevel: 88,
    gpsAccuracyMeters: 4.2,
    networkState: 'ONLINE_4G',
    lastPingSecondsAgo: 1,
    position: { x: 450, y: 140, lat: 13.0827, lng: 80.2707 },
    currentBlockSection: 'MAS-AJJ-DOWN-120',
    envelope: {
      radiusMeters: 600,
      reactionTimeSeconds: 10,
      clearanceBufferMeters: 3.0,
      gpsUncertaintyBufferMeters: 4.2,
      isExpandedDueToGps: false,
    },
  },
  {
    id: 'WRK-102',
    name: 'Suresh Patel',
    role: 'Track Maintainer II',
    teamId: 'TEAM-ALPHA',
    teamName: 'Gang 04 - Chennai Division',
    status: 'SAFE',
    batteryLevel: 74,
    gpsAccuracyMeters: 5.1,
    networkState: 'ONLINE_5G',
    lastPingSecondsAgo: 2,
    position: { x: 470, y: 140, lat: 13.0831, lng: 80.2712 },
    currentBlockSection: 'MAS-AJJ-DOWN-120',
    envelope: {
      radiusMeters: 600,
      reactionTimeSeconds: 10,
      clearanceBufferMeters: 3.0,
      gpsUncertaintyBufferMeters: 5.1,
      isExpandedDueToGps: false,
    },
  },
  {
    id: 'WRK-103',
    name: 'Rajesh Sharma',
    role: 'Track Maintainer III',
    teamId: 'TEAM-ALPHA',
    teamName: 'Gang 04 - Chennai Division',
    status: 'SAFE',
    batteryLevel: 14, // Low battery
    gpsAccuracyMeters: 6.0,
    networkState: 'ONLINE_4G',
    lastPingSecondsAgo: 1,
    position: { x: 490, y: 140, lat: 13.0835, lng: 80.2718 },
    currentBlockSection: 'MAS-AJJ-DOWN-120',
    envelope: {
      radiusMeters: 600,
      reactionTimeSeconds: 10,
      clearanceBufferMeters: 3.0,
      gpsUncertaintyBufferMeters: 6.0,
      isExpandedDueToGps: false,
    },
  },
  {
    id: 'WRK-104',
    name: 'Anil Verma',
    role: 'Welder / Track Maintainer I',
    teamId: 'TEAM-BETA',
    teamName: 'Gang 09 - Arakkonam Section',
    status: 'SAFE',
    batteryLevel: 92,
    gpsAccuracyMeters: 3.8,
    networkState: 'ONLINE_5G',
    lastPingSecondsAgo: 1,
    position: { x: 820, y: 260, lat: 13.0890, lng: 80.2810 },
    currentBlockSection: 'MAS-AJJ-UP-122',
    envelope: {
      radiusMeters: 600,
      reactionTimeSeconds: 10,
      clearanceBufferMeters: 3.0,
      gpsUncertaintyBufferMeters: 3.8,
      isExpandedDueToGps: false,
    },
  },
];

export const INITIAL_TRAINS: Train[] = [
  {
    id: 'TRN-204',
    number: 'EXP-12626',
    name: 'Kerala Superfast Express',
    line: 'DOWN_LINE',
    speedKmh: 110,
    direction: 'WESTBOUND',
    positionX: 50,
    positionY: 140,
    currentBlockSection: 'MAS-AJJ-DOWN-118',
    estimatedStoppingDistanceMeters: 850,
  },
  {
    id: 'TRN-309',
    number: 'SF-12601',
    name: 'Mangalore Mail',
    line: 'UP_LINE',
    speedKmh: 85,
    direction: 'EASTBOUND',
    positionX: 950,
    positionY: 260,
    currentBlockSection: 'MAS-AJJ-UP-124',
    estimatedStoppingDistanceMeters: 620,
  },
];

export const INITIAL_WORK_ZONES: WorkZone[] = [
  {
    id: 'WZ-120',
    code: 'BZ-MAS-120',
    name: 'Km 120/4 - 121/8 Track Packing Work',
    blockSectionCode: 'MAS-AJJ-DOWN-120',
    supervisorName: 'Vikram Singh (JE Track)',
    assignedWorkerIds: ['WRK-101', 'WRK-102', 'WRK-103'],
    status: 'ACTIVE',
    trackSegmentRange: { startX: 430, endX: 520 },
  },
  {
    id: 'WZ-122',
    code: 'BZ-MAS-122',
    name: 'Km 122/2 Thermit Rail Welding',
    blockSectionCode: 'MAS-AJJ-UP-122',
    supervisorName: 'K. V. Raman (SSE Track)',
    assignedWorkerIds: ['WRK-104'],
    status: 'ACTIVE',
    trackSegmentRange: { startX: 800, endX: 860 },
  },
];

export const INITIAL_BLOCK_SECTIONS: BlockSection[] = [
  { code: 'MAS-AJJ-DOWN-118', name: 'Perambur West - Villivakkam Down Line', division: 'Chennai', speedLimitKmh: 110, isOccupied: true, activeTrainId: 'TRN-204' },
  { code: 'MAS-AJJ-DOWN-120', name: 'Villivakkam - Ambattur Down Line', division: 'Chennai', speedLimitKmh: 110, isOccupied: false, activeWorkZoneId: 'WZ-120' },
  { code: 'MAS-AJJ-UP-122', name: 'Ambattur - Avadi Up Line', division: 'Chennai', speedLimitKmh: 110, isOccupied: false, activeWorkZoneId: 'WZ-122' },
  { code: 'MAS-AJJ-UP-124', name: 'Avadi - Pattabiram Up Line', division: 'Chennai', speedLimitKmh: 110, isOccupied: true, activeTrainId: 'TRN-309' },
];

export const INITIAL_SYSTEM_HEALTH: SystemHealthMetric[] = [
  { component: 'API_GATEWAY', status: 'HEALTHY', latencyMs: 24, lastSyncTimestamp: 'Just now' },
  { component: 'WEBSOCKET', status: 'HEALTHY', latencyMs: 18, lastSyncTimestamp: 'Just now' },
  { component: 'POSTGIS_DB', status: 'HEALTHY', latencyMs: 8, lastSyncTimestamp: 'Just now' },
  { component: 'REDIS_STREAM', status: 'HEALTHY', latencyMs: 4, lastSyncTimestamp: 'Just now' },
  { component: 'SIMULATOR', status: 'HEALTHY', latencyMs: 12, lastSyncTimestamp: 'Just now' },
  { component: 'FCM_PUSH', status: 'HEALTHY', latencyMs: 110, lastSyncTimestamp: 'Just now' },
];

export const INITIAL_NEAR_MISSES: NearMissEvent[] = [
  {
    id: 'NM-9021',
    occurredAt: '2026-09-29 11:42:10',
    trainId: 'EXP-12626',
    trainSpeedKmh: 108,
    workerId: 'WRK-101',
    workerName: 'Ramesh Kumar',
    blockSectionCode: 'MAS-AJJ-DOWN-120',
    minSpatialClearanceMeters: 1.8,
    ttdAtAckSeconds: 14,
    severity: 'MODERATE',
    contributingFactors: ['High Wind Noise', 'Curve Section Visibility', 'Late Ack (8s)'],
    locationCoords: { x: 450, y: 140 },
  },
];
