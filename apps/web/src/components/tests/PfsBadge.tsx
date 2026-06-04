// Probabilistic Flakiness Score badge. Severity colors only (no gray):
//   > 85  high-confidence flaky (crit)   ·  20–85 uncertain (warn)  ·  < 20 likely real bug (info)
type Props = { score: number | null };

export function PfsBadge({ score }: Props) {
  if (score === null) {
    return (
      <span className="rounded-full border border-white/20 px-3 py-1 text-[0.875rem] font-semibold text-white/[0.78]">
        No PFS
      </span>
    );
  }
  const tone =
    score > 85 ? "var(--color-crit)" : score < 20 ? "var(--color-info)" : "var(--color-warn)";
  return (
    <span
      className="rounded-full border px-3 py-1 text-[0.875rem] font-semibold"
      style={{ color: tone, borderColor: tone }}
    >
      PFS {score.toFixed(0)}
    </span>
  );
}
