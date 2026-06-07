"use client";

import { motion } from "framer-motion";
import { Search, Stethoscope, Wrench, ShieldCheck, GitPullRequest, Check } from "lucide-react";
import type { ReasoningEvent, StageKey, StageStatus } from "@/lib/types";

const STAGES: { key: StageKey; label: string; icon: typeof Search; from: string }[] = [
  { key: "detect",   label: "Detect",   icon: Search,          from: "system" },
  { key: "diagnose", label: "Diagnose", icon: Stethoscope,     from: "detective" },
  { key: "fix",      label: "Fix",      icon: Wrench,          from: "fixer" },
  { key: "verify",   label: "Verify",   icon: ShieldCheck,     from: "validator" },
  { key: "deliver",  label: "Deliver",  icon: GitPullRequest,  from: "merger" },
];

const ORDER = ["system", "detective", "fixer", "validator", "merger"];






function deriveStatuses(events: ReasoningEvent[]): Record<StageKey, StageStatus> {
  const seen = new Set(events.map((e) => e.stage));
  const errored = events.some((e) => e.type === "error");
  const delivered = events.some((e) => e.type === "merge" && e.mr_iid !== null);
  const done = events.some((e) => e.type === "done") || delivered;

  // The furthest stage that has produced at least one event.
  let maxIdx = -1;
  for (const e of events) {
    const i = ORDER.indexOf(e.stage);
    if (i > maxIdx) maxIdx = i;
  }
  // Detection is implicit (PFS computed before the graph) → mark it reached.
  maxIdx = Math.max(maxIdx, 0);

  const result = {} as Record<StageKey, StageStatus>;
  STAGES.forEach((s, idx) => {
    const reached = idx <= maxIdx;
    if (!reached) result[s.key] = "pending";
    else if (idx < maxIdx || done) result[s.key] = "done";
    else if (errored) result[s.key] = "failed";
    else result[s.key] = "active";
  });
  // detect is always done once any event arrives
  if (seen.size > 0 && result.detect === "active" && maxIdx > 0) result.detect = "done";
  return result;
}

const TONE: Record<StageStatus, string> = {
  pending: "var(--color-text-meta)",
  active: "var(--color-info)",
  done: "var(--color-pass)",
  failed: "var(--color-crit)",
};

export function StageTracker({ events }: { events: ReasoningEvent[] }) {
  const status = deriveStatuses(events);

  return (
    <ol className="mb-6 flex items-center gap-2 rounded-2xl border border-white/[0.14] bg-[#0d0d0f] px-4 py-4">
      {STAGES.map((s, idx) => {
        const st = status[s.key];
        const tone = TONE[st];
        const Icon = st === "done" ? Check : s.icon;
        return (
          <li key={s.key} className="flex flex-1 items-center gap-2">
            <div className="flex items-center gap-2.5">
              <motion.span
                className="grid h-9 w-9 place-items-center rounded-full border-2"
                style={{ borderColor: tone, color: tone }}
                animate={st === "active" ? { scale: [1, 1.12, 1] } : { scale: 1 }}
                transition={st === "active"
                  ? { duration: 1.4, repeat: Infinity, ease: "easeInOut" }
                  : { duration: 0.3 }}
              >
                <Icon size={18} strokeWidth={2.4} aria-hidden />
              </motion.span>
              <span className="text-[0.9375rem] font-semibold" style={{ color: tone }}>
                {s.label}
              </span>
            </div>
            {idx < STAGES.length - 1 && (
              <div className="relative mx-1 h-[3px] flex-1 overflow-hidden rounded-full bg-white/[0.14]">
                <motion.div
                  className="absolute inset-y-0 left-0 rounded-full"
                  style={{ background: "var(--color-pass)" }}
                  initial={{ width: 0 }}
                  animate={{ width: status[STAGES[idx + 1].key] !== "pending" ? "100%" : 0 }}
                  transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
            )}
          </li>
        );
      })}
    </ol>
  );
}
