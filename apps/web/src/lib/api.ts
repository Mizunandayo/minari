import type { DiagnoseAccepted, TestListItem } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const KEY = process.env.NEXT_PUBLIC_DEMO_API_KEY ?? "";

// The demo GitLab project the dashboard diagnoses against.
export const DEMO_PROJECT_ID =
  process.env.NEXT_PUBLIC_DEMO_PROJECT_ID ??
  "francisdanielgenese-group/francisdanielgenese-project";




export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${BASE}/api/v1/healthz`, { cache: "no-store" });
  if (!res.ok) throw new Error(`health ${res.status}`);
  return res.json();
}


export async function getTests(): Promise<TestListItem[]> {
  const res = await fetch(`${BASE}/api/v1/tests`, {
    headers: { "X-API-Key": KEY },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`tests ${res.status}`);
  const body = await res.json();
  return body.data as TestListItem[];
}




export async function startDiagnosis(input: {
  project_id: string; file_path: string; test_name: string; pipeline_id?: number;
}): Promise<DiagnoseAccepted> {
  const res = await fetch(`${BASE}/api/v1/diagnose`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-API-Key": KEY },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error(`diagnose ${res.status}`);
  return res.json();
}





export function streamUrl(streamPath: string, token: string): string {
  return `${BASE}${streamPath}?token=${encodeURIComponent(token)}`;
}
