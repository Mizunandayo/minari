"use client";


import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import type { RootCause, RootCauseSlice } from "@/lib/types";
import { CHART, RAMP } from "./ChartTheme";






const LABEL: Record<RootCause, string> = {
  async: "Async / Timing", race: "Race Condition", resource: "Resource Contention",
  network: "Network Dependency", data: "Data Isolation",
};





export function RootCauseDonut({ data }: { data: RootCauseSlice[] }) {
  const total = data.reduce((s, d) => s + d.count, 0);
  if (total === 0) {
    return (
      <p className="grid h-[260px] place-items-center text-[0.9375rem] font-medium text-white/[0.78]">
        No diagnoses yet. Distribution appears after the first fix.
      </p>
    );
  }
  // Descending by count -> opacity ramp reads as a ranking.
  const sorted = [...data].sort((a, b) => b.count - a.count);


  return (
    <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-center">
      <div className="relative h-[200px] w-[200px] shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={sorted} dataKey="count" nameKey="category"
              cx="50%" cy="50%" innerRadius={62} outerRadius={92}
              paddingAngle={2} stroke="#050505" strokeWidth={3}
              animationDuration={800} animationEasing="ease-out"
            >
              {sorted.map((s, i) => (
                <Cell key={s.category} fill={CHART.info}
                      fillOpacity={RAMP[i] ?? 0.2} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 grid place-items-center">
          <div className="text-center">
            <p className="text-3xl font-bold text-white">{total}</p>
            <p className="text-[0.8125rem] font-medium text-white/[0.78]">diagnoses</p>
          </div>
        </div>
      </div>

      <ul className="w-full space-y-2.5">
        {sorted.map((s, i) => (
          <li key={s.category} className="flex items-center gap-3">
            <span className="h-3 w-3 shrink-0 rounded-sm"
                  style={{ background: CHART.info, opacity: RAMP[i] ?? 0.2 }} aria-hidden />
            <span className="flex-1 text-[0.9375rem] font-medium text-white/[0.92]">
              {LABEL[s.category]}
            </span>
            <span className="text-[0.9375rem] font-semibold text-white">{s.count}</span>
            <span className="w-12 text-right text-[0.875rem] font-medium text-white/[0.78]">
              {Math.round((s.count / total) * 100)}%
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}