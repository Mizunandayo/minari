export type RootCause = "async" | "race" | "resource" | "network" | "data";







export type ReasoningEvent =
  | { type: "mcp_call"; stage: string; ts_ms: number; tool: string; params_summary: string }
  | { type: "mcp_result"; stage: string; ts_ms: number; tool: string; bytes: number; latency_ms: number }
  | { type: "reason"; stage: string; ts_ms: number; text: string }
  | { type: "decide"; stage: string; ts_ms: number; text: string }
  | { type: "verify"; stage: string; ts_ms: number; run_index: number; total_runs: number;
      passed: boolean; duration_ms: number; gate_passed: boolean; variance_reduction_pct: number }
  | { type: "heal"; stage: string; ts_ms: number; attempt: number; reason: string }
  | { type: "merge"; stage: string; ts_ms: number; mr_iid: number | null; mr_url: string | null;
      assigned_to: string | null; detection_confidence: number; diagnosis_confidence: number;
      fix_confidence: number; verification_confidence: number; overall_confidence: number }
  | { type: "done"; stage: string; ts_ms: number; confidence: number; category: RootCause }
  | { type: "error"; stage: string; ts_ms: number; message: string };


export type StageKey = "detect" | "diagnose" | "fix" | "verify" | "deliver";
export type StageStatus = "pending" | "active" | "done" | "failed";

export interface DiagnoseAccepted {
  run_id: string;
  stream_path: string;
  stream_token: string;
}




export interface TestListItem {
  id: string;
  test_name: string;
  file_path: string;
  language: string | null;
  pfs_score: number | null;
  category: RootCause | null;
  confidence: number | null;
}



export type FixCategory = "sync" | "wait" | "isolate" | "timeout" | "resource";

export interface FixCandidate {
  rank: number;
  fix_category: FixCategory;
  confidence: number;
  explanation: string;
  fix_diff: string;
  language: string;
}


export type FixStreamEvent = {
  type: "fix"; stage: string; ts_ms: number; rank: number; fix_category: FixCategory;
  confidence: number; explanation: string; fix_diff: string; language: string;
  syntax_valid: boolean; assertions_safe: boolean;
};


export type AnyStreamEvent = ReasoningEvent | FixStreamEvent;







export interface DashboardSummary {
  tests_fixed: number;
  fixed_this_week: number;
  success_rate: number;        
  flakiness_rate: number;     
  avg_fix_latency_ms: number;
  verifications_total: number;
}

export interface TrendPoint {
  day: string;                
  flakiness_rate: number;     
  runs: number;
}


export interface RootCauseSlice {
  category: RootCause;
  count: number;
}


export interface ActivityItem {
  test_name: string;
  file_path: string;
  category: RootCause | null;
  confidence: number | null;
  mr_iid: number | null;
  mr_url: string | null;
  created_at: string;
}




export type RiskTier = "low" | "elevated" | "high";
export type ForecastTrend = "improving" | "stable" | "worsening";



export interface ForecastItem {
  test_name: string;
  file_path: string;
  predicted_flakiness: number;  
  risk_tier: RiskTier;
  trend: ForecastTrend;
  confidence: number;          
  drivers: string[];
  horizon_days: number;
}


export interface CarbonReport {
  runs_avoided: number;
  ci_minutes_avoided: number;
  energy_kwh: number;
  co2_grams: number;
  engineer_hours_saved: number;
  grid_intensity_g_kwh: number;
  runner_power_kw: number;
}