import { GlassCard } from "./GlassCard";

type Props = { label: string; value: string; trend?: string; severity?: "pass" | "warn" | "crit" };

const severityColor: Record<string, string> = {
  pass: "text-[color:var(--color-pass)]",
  warn: "text-[color:var(--color-warn)]",
  crit: "text-[color:var(--color-crit)]",
};

export function MetricCard({ label, value, trend, severity }: Props) {
  return (
    <GlassCard>
      <p className="text-[0.875rem] font-medium text-white/[0.78]">{label}</p>
      <p className={`mt-3 text-4xl font-bold tracking-tight ${severity ? severityColor[severity] : "text-white"}`}>
        {value}
      </p>
      {trend && <p className="mt-2 text-[0.875rem] font-medium text-white/[0.78]">{trend}</p>}
    </GlassCard>
  );
}
