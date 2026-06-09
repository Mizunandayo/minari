"use client";

import { useEffect, useState } from "react";
import { Clock, GitBranch, Cpu, DollarSign } from "lucide-react";
import type { ReasoningEvent } from "@/lib/types";



// Flash output ~ $0.30 / 1M output tokens. Tokens approximated from streamed reason text.
const USD_PER_TOKEN = 0.30 / 1_000_000;
function approxTokens(events: ReasoningEvent[]): number {
  let chars = 0;
  for (const e of events) if (e.type === "reason") chars += e.text.length;
  return Math.round(chars / 4); // ~4 chars/token, deterministic from real stream
}





function Stat({ icon, label, value }: {
  icon: React.ReactNode; label: string; value: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-white/[0.78]" aria-hidden>{icon}</span>
      <span className="text-[0.875rem] font-medium text-white/[0.78]">{label}</span>
      <span className="font-mono text-[0.9375rem] font-semibold text-white tabular-nums">{value}</span>
    </div>
  );
}

export function PanelStats({ events, running }: {
  events: ReasoningEvent[]; running: boolean;
}) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(id);
  }, [running]);

  if (events.length === 0) return null;

  const first = events[0].ts_ms;
  const last = events[events.length - 1].ts_ms;
  const elapsedMs = running ? Math.max(last - first, now - first) : last - first;
  const mcpCalls = events.filter((e) => e.type === "mcp_call").length;
  const tokens = approxTokens(events);
  const cost = tokens * USD_PER_TOKEN;

  return (
    <div className="flex flex-wrap items-center gap-x-6 gap-y-2 border-b border-white/[0.10] px-5 py-3">
      <Stat icon={<Clock size={16} strokeWidth={2.2} />} label="Elapsed"
        value={`${(elapsedMs / 1000).toFixed(1)}s`} />
      <Stat icon={<GitBranch size={16} strokeWidth={2.2} />} label="MCP calls"
        value={String(mcpCalls)} />
      <Stat icon={<Cpu size={16} strokeWidth={2.2} />} label="Tokens"
        value={`~${tokens.toLocaleString()}`} />
      <Stat icon={<DollarSign size={16} strokeWidth={2.2} />} label="Est. cost"
        value={`$${cost.toFixed(4)}`} />
    </div>
  );
}
