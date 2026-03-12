export type ActivityType = 'Running' | 'Cycling' | 'Swimming' | 'Hiking' | 'Mountain Climbing' | string;

export interface Activity {
  id: number;
  activity_type: ActivityType;
  start_time: string;
  distance_m: number;
  duration_s: number;
  calories_kcal?: number;
  avg_heart_rate?: number;
  max_heart_rate?: number;
  avg_cadence?: number;
  max_cadence?: number;
  avg_stride_length_m?: number;
  total_ascent_m?: number;
  total_descent_m?: number;
  training_load?: number;
  recovery_time_h?: number;
  vo2max?: number;
  source_device?: string;
  polyline?: string;
  is_failed?: boolean;
}

export interface StatsSummary {
  total_activities: number;
  total_distance_km: number;
  total_duration_hours: number;
  total_calories_kcal: number;
}

export interface MonthlyTrend {
  month: string;
  distance_km: number;
  count: number;
  duration_hours: number;
}

export interface TypeDistribution {
  type: string;
  count: number;
}
