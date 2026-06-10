import { Layers, Building2, BadgeCheck, ArrowRight } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const STREAMS = [
  {
    n: "01",
    tag: "Open-core SaaS",
    color: "var(--color-pass)",
    Icon: Layers,
    title: "Free to self-host, paid per active developer",
    body: "The agent is open-core: public repos and self-hosting are free. Teams pay a flat per-developer fee for hosted runs, the live dashboard, forecasting, and the MCP server on private repos.",
    stat: "$25",
    statSub: "/ active dev / mo",
    bullets: [
      "Free: public repos & self-host",
      "Team: private repos, dashboard, forecast",
      "Billed only on developers who actually push",
    ],
  },
  {
    n: "02",
    tag: "Enterprise",
    color: "var(--color-info)",
    Icon: Building2,
    title: "Self-hosted, SSO, audit, and an SLA",
    body: "Regulated and large orgs license a self-hosted deployment with SSO/SAML, audit logging, private model routing, and a support SLA. Annual contracts, seat- or org-based.",
    stat: "Custom",
    statSub: "annual contract",
    bullets: [
      "SSO/SAML + audit logs",
      "Private model routing, data stays in-VPC",
      "Priority support & onboarding SLA",
    ],
  },
  {
    n: "03",
    tag: "Outcome-based",
    color: "var(--color-warn)",
    Icon: BadgeCheck,
    title: "Pay only for fixes that actually verify",
    body: "An optional usage add-on prices Minari on value delivered: a fee per verified fix merged. Because the safety gate ships only 5/5-green fixes, customers pay strictly for repairs that worked.",
    stat: "per fix",
    statSub: "value-aligned add-on",
    bullets: [
      "Charged on verified, merged fixes only",
      "Inference cost is cents, high gross margin",
      "Price scales with proven impact",
    ],
  },
];

const PATH = [
  { label: "OSS / self-host", sub: "Free", color: "var(--color-pass)" },
  { label: "Team plan", sub: "$25 / dev / mo", color: "var(--color-info)" },
  { label: "Outcome add-on", sub: "per verified fix", color: "var(--color-warn)" },
  { label: "Enterprise", sub: "self-hosted + SLA", color: "var(--color-crit)" },
];

export function Revenue() {
  return (
    <section id="revenue" className="relative z-10 overflow-hidden py-32" style={{ background: "#070707" }}>
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{ background: "radial-gradient(ellipse 55% 35% at 50% 0%, rgba(52,211,153,0.05) 0%, transparent 70%)" }}
      />
      <div className="relative z-10 mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Business Model</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-5">
            Three revenue streams.
            <br />
            <span className="text-white/[0.48]">Priced on value, not promises.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-14 max-w-3xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            Open-core adoption seeds teams for free, a per-developer plan monetises private repos,
            and an outcome-based add-on ties price directly to verified fixes shipped.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
          {STREAMS.map((s, i) => (
            <Reveal key={s.n} delay={(i + 1) as 1 | 2 | 3}>
              <div
                className="flex h-full flex-col overflow-hidden rounded-2xl border"
                style={{ borderColor: `color-mix(in srgb, ${s.color} 32%, transparent)`, background: "#0a0a0e" }}
              >
                <div
                  className="border-b p-6"
                  style={{
                    borderColor: `color-mix(in srgb, ${s.color} 32%, transparent)`,
                    background: `color-mix(in srgb, ${s.color} 10%, transparent)`,
                  }}
                >
                  <div className="mb-4 flex items-start justify-between">
                    <span
                      className="flex items-center justify-center rounded-xl border"
                      style={{ width: 52, height: 52, borderColor: `color-mix(in srgb, ${s.color} 32%, transparent)`, background: `color-mix(in srgb, ${s.color} 14%, transparent)` }}
                    >
                      <s.Icon size={24} strokeWidth={2} style={{ color: s.color }} aria-hidden />
                    </span>
                    <div className="text-right">
                      <div className="font-bold leading-none tracking-[-0.04em]" style={{ fontSize: "clamp(1.6rem,3vw,2.2rem)", color: s.color }}>
                        {s.stat}
                      </div>
                      <div className="mt-1 text-[0.72rem] font-semibold text-white/[0.78]">{s.statSub}</div>
                    </div>
                  </div>
                  <div className="mb-2 text-[0.7rem] font-bold uppercase tracking-[0.14em]" style={{ color: s.color }}>
                    {s.n} · {s.tag}
                  </div>
                  <div className="text-[1.05rem] font-bold leading-snug text-white">{s.title}</div>
                </div>

                <div className="flex flex-1 flex-col gap-5 p-6">
                  <p className="text-[0.88rem] leading-relaxed text-white/[0.92]">{s.body}</p>
                  <div className="mt-auto flex flex-col gap-2.5">
                    {s.bullets.map((b) => (
                      <div key={b} className="flex items-start gap-2.5">
                        <BadgeCheck size={15} strokeWidth={2.2} className="mt-[2px] shrink-0" style={{ color: s.color }} aria-hidden />
                        <span className="text-[0.85rem] leading-relaxed text-white/[0.92]">{b}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Conversion path */}
        <Reveal delay={4}>
          <div className="glass-panel mt-8 rounded-2xl p-6">
            <div className="mb-4 text-[0.72rem] font-bold uppercase tracking-[0.12em] text-white/[0.78]">
              Natural upgrade path
            </div>
            <div className="flex items-center gap-0 overflow-auto">
              {PATH.map((step, i) => (
                <div key={step.label} className="flex min-w-0 items-center">
                  <div
                    className="flex flex-col items-center gap-1.5 rounded-xl border px-5 py-3"
                    style={{ minWidth: 150, borderColor: `color-mix(in srgb, ${step.color} 40%, transparent)`, background: `color-mix(in srgb, ${step.color} 9%, transparent)` }}
                  >
                    <div className="text-[0.85rem] font-bold text-white">{step.label}</div>
                    <div className="text-[0.72rem] font-semibold" style={{ color: step.color }}>{step.sub}</div>
                  </div>
                  {i < PATH.length - 1 && (
                    <ArrowRight size={18} strokeWidth={2} className="mx-2 shrink-0 text-white/[0.48]" aria-hidden />
                  )}
                </div>
              ))}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
