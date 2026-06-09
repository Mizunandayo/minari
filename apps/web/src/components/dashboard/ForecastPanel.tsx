import { TrendingDown, TrendingUp, Minus } from "lucide-react";
import { getDashboardForecast } from "@/lib/api";
import type { ForecastItem, ForecastTrend } from "@/lib/types";
import { RiskTierBadge } from "@/components/ui/RiskTierBadge";


const TREND_ICON: Record<ForecastTrend, typeof Minus> = {
  improving: TrendingDown,  
  stable: Minus,
  worsening: TrendingUp,
};
const TREND_COLOR: Record<ForecastTrend, string> = {
  improving: "var(--color-pass)",
  stable: "var(--color-text-meta)",
  worsening: "var(--color-crit)",
};





export async function ForecastPanel() {
  let items: ForecastItem[] = [];
  try { items = await getDashboardForecast(); } catch { items = []; }

  if (items.length === 0) {
    return (
      <div className="rounded-2xl border border-white/[0.14] bg-white/[0.035] px-6 py-8">
        <p className="text-[0.9375rem] font-semibold text-white/[0.92]">
          No forecast yet — run the pipeline so Minari can learn each test&apos;s history.
        </p>
      </div>
    );
  }





  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {items.slice(0, 6).map((it, i) => {
        const Trend = TREND_ICON[it.trend];
        const pct = Math.round(it.predicted_flakiness * 100);
        return (
          <article
            key={it.file_path + it.test_name}
            className="rounded-2xl border border-white/[0.14] bg-white/[0.035] p-6
                       transition-transform duration-300 ease-out hover:-translate-y-0.5
                       motion-safe:animate-[fadeUp_.5s_ease-out_both]"
            style={{ animationDelay: `${i * 60}ms` }}
          >
            <div className="flex items-start justify-between gap-4">
              <p className="font-mono text-[0.9375rem] font-semibold text-white">
                {it.test_name}
              </p>
              <RiskTierBadge tier={it.risk_tier} />
            </div>

            <div className="mt-5 flex items-end gap-3">
              <span className="text-4xl font-bold tracking-tight text-white">{pct}%</span>
              <span className="mb-1 inline-flex items-center gap-1.5 text-[0.875rem] font-semibold"
                    style={{ color: TREND_COLOR[it.trend] }}>
                <Trend size={16} strokeWidth={2.4} aria-hidden />
                {it.trend}
              </span>
            </div>
            <p className="mt-1 text-[0.875rem] font-normal text-white/[0.78]">
              projected flaky-run probability over the next {it.horizon_days} days
            </p>

            <ul className="mt-4 space-y-1.5">
              {it.drivers.slice(0, 2).map((d) => (
                <li key={d} className="text-[0.875rem] font-normal text-white/[0.92]">— {d}</li>
              ))}
            </ul>
          </article>
        );
      })}
    </div>
  );
}
