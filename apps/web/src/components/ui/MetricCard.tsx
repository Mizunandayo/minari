import { GlassCard } from "./GlassCard";

type Props = { label: string; value: string; trend?: string; severity?: "pass" | "warn" | "crit" };

const severityColor: Record<string, string> = {
  pass: "text-pass",
  warn: "text-warn",
  crit: "text-crit",
};

export function MetricCard({ label, value, trend, severity }: Props) {
  return (
    <GlassCard>
      <p className="text-[0.875rem] font-semibold tracking-wide text-ink-muted uppercase">{label}</p>
      <p className={`mt-3 text-4xl font-bold tracking-tight ${severity ? severityColor[severity] : "text-ink"}`}>
        {value}
      </p>
      {trend && <p className="mt-2 text-[0.875rem] font-medium text-ink-muted">{trend}</p>}
    </GlassCard>
  );
}
