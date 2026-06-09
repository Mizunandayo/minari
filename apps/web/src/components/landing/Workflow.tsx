"use client";

import { useEffect, useState } from "react";
import { ScanSearch, Stethoscope, Wrench, ShieldCheck, GitMerge } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const STEPS = [
  { n: "01", name: "Detect", sub: "Score flakiness from history", tech: "PFS engine", Icon: ScanSearch, color: "var(--color-info)" },
  { n: "02", name: "Diagnose", sub: "Find the real root cause", tech: "Gemini 2.5 · pgvector", Icon: Stethoscope, color: "var(--color-info)" },
  { n: "03", name: "Fix", sub: "Write ranked candidate repairs", tech: "tree-sitter gates", Icon: Wrench, color: "var(--color-warn)" },
  { n: "04", name: "Verify", sub: "Prove it in real CI, 5× over", tech: "GitLab pipelines", Icon: ShieldCheck, color: "var(--color-pass)" },
  { n: "05", name: "Deliver", sub: "Open a reviewed merge request", tech: "GitLab MCP", Icon: GitMerge, color: "var(--color-pass)" },
];

export function Workflow() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setActive((p) => (p + 1) % STEPS.length), 1400);
    return () => clearInterval(t);
  }, []);

  return (
    <section id="workflow" className="relative z-10 py-32" style={{ background: "#050505" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>How It Works</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-4">
            One trigger.
            <br />
            <span className="text-white/[0.48]">The entire repair, end to end.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-8 max-w-2xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            Detect → Diagnose → Fix → Verify → Deliver. Five specialist agents, one LangGraph
            pipeline, no human in the loop until the merge request is ready for review.
          </p>
        </Reveal>

        <Reveal delay={3}>
          <div className="glass-panel mb-8 rounded-2xl p-4">
            <div className="flow-lane mb-2">
              <span className="flow-pulse" />
              <span className="flow-pulse d1" />
              <span className="flow-pulse d2" />
            </div>
            <p className="text-center text-[0.9rem] text-white/[0.78]">
              Continuous data flow from a flaky run to a verified, reviewed merge request.
            </p>
          </div>
        </Reveal>

        <Reveal delay={4}>
          <div className="glass-panel overflow-auto rounded-2xl p-2">
            <div className="flex min-w-[720px] items-stretch">
              {STEPS.map((s, i) => {
                const state = i === active ? "active" : i < active ? "passed" : "idle";
                return (
                  <div key={s.n} className="flex flex-1 items-center">
                    <div className="relative flex flex-1 flex-col items-center px-3 py-7 text-center">
                      {i > 0 && (
                        <span
                          className="absolute left-0 top-1/2 h-px w-1/2 -translate-y-1/2 transition-all duration-500"
                          style={{
                            background: i <= active ? "rgba(255,255,255,0.85)" : "rgba(255,255,255,0.14)",
                            boxShadow: i <= active ? "0 0 8px rgba(255,255,255,0.35)" : "none",
                          }}
                        />
                      )}
                      {i < STEPS.length - 1 && (
                        <span
                          className="absolute right-0 top-1/2 h-px w-1/2 -translate-y-1/2 transition-all duration-500"
                          style={{
                            background: i < active ? "rgba(255,255,255,0.85)" : "rgba(255,255,255,0.14)",
                            boxShadow: i < active ? "0 0 8px rgba(255,255,255,0.35)" : "none",
                          }}
                        />
                      )}
                      <div
                        className={`relative z-10 mb-3 flex h-12 w-12 items-center justify-center rounded-full border transition-all duration-300 ${
                          state === "active" ? "pipe-active" : state === "passed" ? "pipe-passed" : "border-white/25"
                        }`}
                      >
                        <s.Icon size={20} strokeWidth={2.2} style={{ color: s.color }} aria-hidden />
                      </div>
                      <div className={`mb-1 text-[0.82rem] font-bold tracking-wide ${i === active ? "text-white" : "text-white/[0.78]"}`}>
                        {s.n}
                      </div>
                      <div className={`mb-1.5 text-[0.96rem] font-bold ${i === active ? "text-white" : "text-white/[0.92]"}`}>
                        {s.name}
                      </div>
                      <div className="mb-2 text-[0.85rem] font-medium text-white/[0.78]">{s.sub}</div>
                      <div
                        className={`rounded border px-2 py-0.5 text-[0.8rem] font-semibold transition-all duration-300 ${
                          i === active ? "border-white/40 bg-white/[0.12] text-white" : "border-white/20 text-white/[0.78]"
                        }`}
                      >
                        {s.tech}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
