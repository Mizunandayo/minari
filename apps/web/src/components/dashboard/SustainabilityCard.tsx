import { Leaf, Clock, Cpu } from "lucide-react";
import { getDashboardSustainability } from "@/lib/api";
import type { CarbonReport } from "@/lib/types";




function fmtCo2(grams: number) {
  return grams >= 1000 ? `${(grams / 1000).toFixed(2)} kg` : `${grams.toFixed(0)} g`;
}





export async function SustainabilityCard() {
  let r: CarbonReport | null = null;
  try { r = await getDashboardSustainability(); } catch { r = null; }
  if (!r) return null;

  const stats = [
    { Icon: Leaf, color: "var(--color-pass)", value: fmtCo2(r.co2_grams), label: "CO₂e avoided" },
    { Icon: Cpu, color: "var(--color-info)", value: `${r.ci_minutes_avoided.toFixed(0)} min`, label: "CI compute saved" },
    { Icon: Clock, color: "var(--color-warn)", value: `${r.engineer_hours_saved} h`, label: "engineer time reclaimed" },
  ];

  return (
    <div className="rounded-2xl border border-white/[0.14] bg-white/[0.035] p-6 sm:p-8">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        {stats.map(({ Icon, color, value, label }) => (
          <div key={label} className="flex items-center gap-4">
            <span className="grid h-12 w-12 place-items-center rounded-xl"
                  style={{ backgroundColor: `${color}1f`, border: `1px solid ${color}40` }}>
              <Icon size={22} strokeWidth={2.2} style={{ color }} aria-hidden />
            </span>
            <div>
              <p className="text-2xl font-bold tracking-tight text-white">{value}</p>
              <p className="text-[0.875rem] font-normal text-white/[0.78]">{label}</p>
            </div>
          </div>
        ))}
      </div>
      <p className="mt-6 text-[0.875rem] font-normal text-white/[0.78]">
        Estimated from {r.runs_avoided} avoided flaky CI re-runs, at{" "}
        {r.grid_intensity_g_kwh} gCO₂e/kWh grid intensity and {r.runner_power_kw} kW runner draw.
        Conservative by design.
      </p>
    </div>
  );
}
