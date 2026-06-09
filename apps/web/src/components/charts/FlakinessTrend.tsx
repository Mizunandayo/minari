"use client";


import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer,
  Tooltip, XAxis, YAxis,
} from "recharts";
import type { TrendPoint } from "@/lib/types";
import { CHART } from "./ChartTheme";






function pct(v: number) { return `${Math.round(v * 100)}%`; }
function shortDay(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}




function TrendTooltip({ active, payload }: {
  active?: boolean; payload?: Array<{ payload: TrendPoint }>;
}) {
  if (!active || !payload?.length) return null;
  const p = payload[0].payload;
  return (
    <div className="rounded-xl border border-white/[0.14] bg-[#0d0d0f] px-4 py-3 shadow-xl">
      <p className="text-[0.875rem] font-semibold text-white">{shortDay(p.day)}</p>
      <p className="mt-1 text-[0.9375rem] font-bold" style={{ color: CHART.info }}>
        {pct(p.flakiness_rate)} flaky
      </p>
      <p className="text-[0.8125rem] font-medium text-white/[0.78]">{p.runs} runs</p>
    </div>
  );
}





export function FlakinessTrend({ data }: { data: TrendPoint[] }) {
  if (data.length === 0) {
    return (
      <p className="grid h-[260px] place-items-center text-[0.9375rem] font-medium text-white/[0.78]">
        No run history yet. Trends appear once tests start executing.
      </p>
    );
  }
  return (
    <div className="h-[260px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 4, left: -12 }}>
          <defs>
            <linearGradient id="flakFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={CHART.info} stopOpacity={0.32} />
              <stop offset="100%" stopColor={CHART.info} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke={CHART.grid} vertical={false} />
          <XAxis
            dataKey="day" tickFormatter={shortDay} tick={CHART.axisTick}
            tickLine={false} axisLine={{ stroke: CHART.grid }} minTickGap={28}
          />
          <YAxis
            tickFormatter={pct} tick={CHART.axisTick} tickLine={false}
            axisLine={false} width={48} domain={[0, "auto"]}
          />
          <Tooltip content={<TrendTooltip />} cursor={{ stroke: CHART.grid }} />
          <Area
            type="monotone" dataKey="flakiness_rate" stroke={CHART.info}
            strokeWidth={2.5} fill="url(#flakFill)"
            animationDuration={900} animationEasing="ease-out"
            activeDot={{ r: 5, fill: CHART.info, stroke: "#050505", strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}