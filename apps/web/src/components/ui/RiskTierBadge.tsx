import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";
import type { RiskTier } from "@/lib/types";



const MAP: Record<RiskTier, { label: string; color: string; Icon: typeof ShieldCheck }> = {
  low:      { label: "Low risk",      color: "var(--color-pass)", Icon: ShieldCheck },
  elevated: { label: "Elevated risk", color: "var(--color-warn)", Icon: ShieldAlert },
  high:     { label: "High risk",     color: "var(--color-crit)", Icon: ShieldX },
};






export function RiskTierBadge({ tier }: { tier: RiskTier }) {
  const { label, color, Icon } = MAP[tier];
  return (
    <span
      className="inline-flex items-center gap-2 rounded-full px-3 py-1 text-[0.8125rem] font-semibold"
      style={{ color, backgroundColor: `${color}1f`, border: `1px solid ${color}40` }}
    >
      <Icon size={15} strokeWidth={2.4} aria-hidden />
      {label}
    </span>
  );
}
