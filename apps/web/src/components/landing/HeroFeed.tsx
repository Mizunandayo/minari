"use client";

import { motion } from "framer-motion";

type Severity = "crit" | "warn" | "info" | "pass";

// Representative feed of the demo project's tracked tests, ranked by flakiness
// risk. Mirrors what the live dashboard surfaces — category, id, test, score.
const FEED: { code: string; id: string; test: string; score: number; sev: Severity }[] = [
  { code: "ASYNC", id: "T-2847", test: "test_async_result_ready_after_sleep", score: 94, sev: "crit" },
  { code: "RACE", id: "T-1823", test: "test_event_order_dependent_result", score: 78, sev: "warn" },
  { code: "RES", id: "T-0042", test: "test_pool_acquire_under_contention", score: 71, sev: "warn" },
  { code: "NET", id: "T-8807", test: "test_service_responds_within_latency_budget", score: 55, sev: "info" },
  { code: "DATA", id: "T-1142", test: "test_cart_total_isolation", score: 28, sev: "pass" },
];

const SEV: Record<Severity, string> = {
  crit: "var(--color-crit)",
  warn: "var(--color-warn)",
  info: "var(--color-info)",
  pass: "var(--color-pass)",
};

export function HeroFeed() {
  return (
    <div className="text-left">
      {/* Terminal card */}
      <div className="overflow-hidden rounded-2xl border border-white/[0.14] bg-[#08080a] shadow-[0_24px_80px_-24px_rgba(0,0,0,0.9)]">
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-white/[0.1] px-5 py-3.5">
          <span className="flex gap-1.5" aria-hidden>
            <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-crit)" }} />
            <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-warn)" }} />
            <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-pass)" }} />
          </span>
          <span className="text-[0.82rem] font-medium tracking-[-0.01em] text-white/[0.78]">
            minari — live agent feed
          </span>
          <span className="ml-auto inline-flex items-center gap-2 text-[0.7rem] font-bold uppercase tracking-[0.16em] text-white/[0.78]">
            <motion.span
              className="h-2 w-2 rounded-full"
              style={{ background: "var(--color-pass)" }}
              animate={{ opacity: [1, 0.25, 1] }}
              transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
              aria-hidden
            />
            Live
          </span>
        </div>

        {/* Rows */}
        <ul>
          {FEED.map((f, i) => (
            <motion.li
              key={f.test}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 + i * 0.12, duration: 0.4, ease: "easeOut" }}
              className="flex items-center gap-3 border-b border-white/[0.06] px-5 py-3.5 last:border-b-0"
              style={{ borderLeft: `2px solid ${SEV[f.sev]}` }}
            >
              <span
                className="w-12 shrink-0 text-[0.72rem] font-bold uppercase tracking-[0.06em]"
                style={{ color: SEV[f.sev] }}
              >
                {f.code}
              </span>
              <span className="hidden w-14 shrink-0 text-[0.78rem] font-medium text-white/[0.78] sm:block">
                {f.id}
              </span>
              <span className="truncate text-[0.82rem] font-medium text-white">{f.test}</span>
              <span
                className="ml-auto shrink-0 text-[0.95rem] font-bold tabular-nums"
                style={{ color: SEV[f.sev] }}
              >
                {f.score}
              </span>
            </motion.li>
          ))}
        </ul>

        {/* Caption */}
        <div className="border-t border-white/[0.1] px-5 py-3 text-[0.78rem] font-medium text-white/[0.78]">
          Ranked by flakiness risk · diagnosed, fixed &amp; verified autonomously over GitLab MCP
        </div>
      </div>
    </div>
  );
}
