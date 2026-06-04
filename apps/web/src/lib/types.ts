export type RootCause = "async" | "race" | "resource" | "network" | "data";






export type ReasoningEvent =
  | { type: "mcp_call"; stage: string; ts_ms: number; tool: string; params_summary: string }
  | { type: "mcp_result"; stage: string; ts_ms: number; tool: string; bytes: number; latency_ms: number }
  | { type: "reason"; stage: string; ts_ms: number; text: string }
  | { type: "decide"; stage: string; ts_ms: number; text: string }
  | { type: "done"; stage: string; ts_ms: number; confidence: number; category: RootCause }
  | { type: "error"; stage: string; ts_ms: number; message: string };



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