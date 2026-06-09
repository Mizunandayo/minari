import { Check } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const PHASES = [
  {
    num: "1",
    phase: "Phase 1",
    when: "Now — Live",
    color: "var(--color-pass)",
    done: true,
    title: "Autonomous repair, end to end",
    items: [
      "Five-stage LangGraph pipeline live on Cloud Run + Vercel",
      "Python / pytest with real GitLab CI verification (5× runs)",
      "Assertion-safety gate + confidence cascade, never auto-merges",
      "Live dashboard, predictive forecast, sustainability tracker",
      "Minari exposed as its own MCP server",
    ],
  },
  {
    num: "2",
    phase: "Phase 2",
    when: "~1 quarter",
    color: "var(--color-info)",
    done: false,
    title: "More languages, more platforms",
    items: [
      "JavaScript / TypeScript (Jest, Vitest) and Go support",
      "GitHub Actions alongside GitLab CI",
      "Persistent MCP session to shave seconds per run",
      "Org-wide flakiness analytics across repos",
      "Slack + merge-request annotations on every fix",
    ],
  },
  {
    num: "3",
    phase: "Phase 3",
    when: "~2–3 quarters",
    color: "var(--color-warn)",
    done: false,
    title: "From repair to prevention",
    items: [
      "Forecast-driven pre-merge flakiness gating",
      "Auto-quarantine with batched, scheduled fix MRs",
      "Self-hosted enterprise: SSO, audit, private routing",
      "Fine-tuned diagnosis on accumulated repair history",
      "Shared library of verified fix strategies",
    ],
  },
];

const IMPACT = [
  {
    label: "Scalability",
    color: "var(--color-pass)",
    title: "Stateless agents, serverless-ready",
    body: "Each run is independent and short-lived. Cloud Run scales horizontally; Redis holds shared limits. No per-customer infrastructure to babysit.",
  },
  {
    label: "Moat",
    color: "var(--color-info)",
    title: "Verification + a diagnosis flywheel",
    body: "Real-CI proof and the assertion-safety gate are hard to copy. Every diagnosis enriches the similarity store, so accuracy compounds with usage.",
  },
  {
    label: "Impact",
    color: "var(--color-warn)",
    title: "Detection was the start, not the goal",
    body: "Competitors flag flakiness; Minari removes it and is moving toward preventing it — closing the loop the rest of the category leaves open.",
  },
];

export function Roadmap() {
  return (
    <section id="roadmap" className="relative z-10 overflow-hidden py-32" style={{ background: "#050505" }}>
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{ background: "radial-gradient(ellipse 60% 40% at 50% 0%, rgba(255,255,255,0.025) 0%, transparent 70%)" }}
      />
      <div className="relative z-10 mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Roadmap</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-5">
            Live today.
            <br />
            <span className="text-white/[0.48]">Built to become a platform.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-14 max-w-3xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            The five-stage pipeline ships verified fixes today. From here, Minari widens across
            languages and platforms, then shifts from repairing flakiness to preventing it.
          </p>
        </Reveal>

        {/* Timeline nodes */}
        <Reveal delay={2}>
          <div className="relative mb-8 flex items-start justify-between">
            <div
              className="absolute hidden md:block"
              style={{
                top: 19,
                left: "16.5%",
                right: "16.5%",
                height: 2,
                background:
                  "linear-gradient(90deg, var(--color-pass) 0%, var(--color-info) 50%, var(--color-warn) 100%)",
              }}
              aria-hidden
            />
            {PHASES.map((p) => (
              <div key={p.phase} className="flex flex-1 flex-col items-center gap-3">
                <div
                  className="relative z-10 flex h-10 w-10 items-center justify-center rounded-full font-bold"
                  style={{
                    background: p.done ? p.color : "#111",
                    border: `2px solid ${p.color}`,
                    color: p.done ? "#050505" : p.color,
                    boxShadow: `0 0 22px color-mix(in srgb, ${p.color} 55%, transparent)`,
                  }}
                >
                  {p.done ? <Check size={18} strokeWidth={2.6} aria-hidden /> : p.num}
                </div>
                <div className="text-center">
                  <div className="text-[0.66rem] font-bold uppercase tracking-[0.14em]" style={{ color: p.color }}>
                    {p.phase}
                  </div>
                  <div className="text-[0.78rem] font-medium text-white/[0.78]">{p.when}</div>
                </div>
              </div>
            ))}
          </div>
        </Reveal>

        {/* Phase cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
          {PHASES.map((p, i) => (
            <Reveal key={p.phase} delay={(i + 1) as 1 | 2 | 3}>
              <div
                className="flex h-full flex-col gap-4 rounded-2xl border p-6"
                style={{ borderColor: `color-mix(in srgb, ${p.color} 32%, transparent)`, background: `color-mix(in srgb, ${p.color} 7%, transparent)` }}
              >
                <div className="text-[1rem] font-bold text-white">{p.title}</div>
                <ul className="flex flex-col gap-2.5">
                  {p.items.map((item) => (
                    <li key={item} className="flex items-start gap-2.5">
                      <Check size={15} strokeWidth={2.4} className="mt-[2px] shrink-0" style={{ color: p.color }} aria-hidden />
                      <span className="text-[0.86rem] leading-relaxed text-white/[0.92]">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Impact summary */}
        <Reveal delay={3}>
          <div className="glass-panel overflow-hidden rounded-2xl">
            <div className="grid grid-cols-1 divide-y divide-white/[0.1] md:grid-cols-3 md:divide-x md:divide-y-0">
              {IMPACT.map((item) => (
                <div key={item.label} className="p-7">
                  <div className="mb-3 text-[0.66rem] font-bold uppercase tracking-[0.14em]" style={{ color: item.color }}>
                    {item.label}
                  </div>
                  <div className="mb-2 text-[0.96rem] font-bold text-white">{item.title}</div>
                  <div className="text-[0.88rem] leading-relaxed text-white/[0.92]">{item.body}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
