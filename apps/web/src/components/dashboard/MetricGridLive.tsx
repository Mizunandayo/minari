import { MetricCard } from "@/components/ui/MetricCard";
import { getDashboardSummary } from "@/lib/api";
import type { DashboardSummary } from "@/lib/types";




function fmtSeconds(ms: number) {
  return ms >= 1000 ? `${(ms / 1000).toFixed(1)}s` : `${ms}ms`;
}

export async function MetricGridLive() {
  let s: DashboardSummary | null = null;
  try { s = await getDashboardSummary(); } catch { s = null; }

  if (!s) {
    return (
      <section className="rounded-2xl border border-white/[0.14] bg-white/[0.035] px-6 py-8">
        <p className="text-[0.9375rem] font-semibold text-white/[0.92]">
          Metrics unavailable — is the Minari API running on :8000?
        </p>
      </section>
    );
  }

  const success = Math.round(s.success_rate * 100);
  const flak = (s.flakiness_rate * 100).toFixed(1);
  // Don't render a misleading "0ms" when no latency was recorded yet.
  const latency = s.avg_fix_latency_ms > 0 ? fmtSeconds(s.avg_fix_latency_ms) : "—";

  return (
    <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard label="Tests Fixed" value={String(s.tests_fixed)}
        trend={`+${s.fixed_this_week} this week`} severity="pass" />
      <MetricCard label="Avg Diagnosis Time" value={latency}
        trend={latency === "—" ? "no timing recorded yet" : "agent reasoning latency"} />
      <MetricCard label="Verification Success" value={`${success}%`}
        trend={`${s.verifications_total} runs`} severity={success >= 80 ? "pass" : "warn"} />
      <MetricCard label="Flakiness Rate" value={`${flak}%`}
        trend="trending down" severity={s.flakiness_rate <= 0.1 ? "pass" : "warn"} />
    </section>
  );
}