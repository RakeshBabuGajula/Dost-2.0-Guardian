export interface LocationPoint {
  latitude: number;
  longitude: number;
}

export interface SpatialWorkerResult {
  id: string;
  name: string;
  role: string;
  team_id?: string;
  status: string;
  current_block_section: string;
  distance_meters: number;
  latitude: number;
  longitude: number;
  gps_accuracy_meters: number;
  last_updated_at: string;
}

export interface SpatialTrainResult {
  id: string;
  number: string;
  name: string;
  line: string;
  speed_kmh: number;
  heading: number;
  direction: string;
  current_block_section: string;
  distance_meters: number;
  latitude: number;
  longitude: number;
  last_updated_at: string;
}

export interface RefugeResult {
  id: string;
  code: string;
  name: string;
  refuge_type: string;
  capacity_persons: number;
  distance_meters: number;
  latitude: number;
  longitude: number;
}

export interface BlockContextResult {
  code: string;
  name: string;
  line_type: string;
  speed_limit_kmh: number;
  status: string;
  candidate_blocks: string[];
  is_ambiguous: boolean;
}

export interface TrackSegmentResult {
  id: string;
  code: string;
  name: string;
  track_code: string;
  direction: string;
  chainage_start_km: number;
  chainage_end_km: number;
  speed_limit_kmh: number;
  distance_meters: number;
}

export interface SpatialWorkerContext {
  worker_id: string;
  worker_name: string;
  current_location: LocationPoint;
  containing_block?: BlockContextResult;
  containing_work_zone?: {
    id: string;
    name: string;
    assigned_team_code: string;
    status: string;
  };
  nearest_refuge?: RefugeResult;
  nearby_trains: SpatialTrainResult[];
}
