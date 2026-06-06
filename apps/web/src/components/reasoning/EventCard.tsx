"use client";

import { motion } from "framer-motion";
import { Terminal, Database, Brain, GitBranch, CheckCircle2, AlertTriangle, ShieldCheck, Wrench } from "lucide-react";
import type { ReasoningEvent } from "@/lib/types";




const META: Record<ReasoningEvent["type"], { icon: typeof Terminal; label: string; tone: string }> = {
  mcp_call:   { icon: GitBranch,    label: "MCP CALL",   tone: "var(--color-info)" },
  mcp_result: { icon: Database,     label: "MCP RESULT", tone: "var(--color-info)" },
  reason:     { icon: Brain,        label: "REASON",     tone: "var(--color-text)" },
  decide:     { icon: Terminal,     label: "DECIDE",     tone: "var(--color-warn)" },
  verify:     { icon: ShieldCheck,  label: "VERIFY",     tone: "var(--color-pass)" },
  heal:       { icon: Wrench,       label: "SELF-HEAL",  tone: "var(--color-warn)" },
  done:       { icon: CheckCircle2, label: "DONE",       tone: "var(--color-pass)" },
  error:      { icon: AlertTriangle,label: "ERROR",      tone: "var(--color-crit)" },
};





function body(e: ReasoningEvent): string {
  switch (e.type) {
    case "mcp_call":   return `${e.tool}(${e.params_summary})`;
    case "mcp_result": return `${e.tool} → ${e.bytes} bytes · ${e.latency_ms}ms`;
    case "reason":     return e.text;
    case "decide":     return e.text;
    case "verify":     return `Run ${e.run_index}/${e.total_runs}: ${e.passed ? "PASS" : "FAIL"}`
                            + ` · ${e.duration_ms.toFixed(0)}ms`
                            + (e.run_index === e.total_runs
                                ? ` · gate ${e.gate_passed ? "PASSED" : "FAILED"}`
                                  + ` · variance −${(e.variance_reduction_pct * 100).toFixed(0)}%`
                                : "");
    case "heal":       return `Attempt ${e.attempt}: ${e.reason}`;
    case "done":       return `Diagnosis complete · ${e.category} · confidence ${(e.confidence * 100).toFixed(0)}%`;
    case "error":      return e.message;
  }
}




export function EventCard({ event }: { event: ReasoningEvent }) {
  const meta = META[event.type];
  // A failed verification run flips to the crit tone so red/green reads at a glance.
  const tone = event.type === "verify" && !event.passed ? "var(--color-crit)" : meta.tone;
  const Icon = meta.icon;
  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
      className="flex items-start gap-3 border-l-2 py-2.5 pl-4"
      style={{ borderColor: tone }}
    >
      <Icon size={18} strokeWidth={2.2} aria-hidden style={{ color: tone, flexShrink: 0, marginTop: 2 }} />
      <div className="min-w-0">
        <span className="text-[0.875rem] font-semibold tracking-wide" style={{ color: tone }}>
          {meta.label}
        </span>
        <p className="font-mono text-[0.9375rem] leading-relaxed text-white/[0.92] break-words">
          {body(event)}
        </p>
      </div>
    </motion.div>
  );
}
