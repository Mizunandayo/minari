import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const SEGMENTS = [
  {
    key: "TAM",
    value: "$48B",
    color: "var(--color-info)",
    title: "Software testing & quality tooling",
    body: "The global market for test automation and developer quality tools, projected through 2030.",
  },
  {
    key: "SAM",
    value: "$6B",
    color: "var(--color-warn)",
    title: "CI-integrated test reliability",
    body: "Teams on Git-based CI who feel flakiness directly, the slice Minari plugs into natively.",
  },
  {
    key: "SOM",
    value: "$120M",
    color: "var(--color-pass)",
    title: "GitLab-native orgs with active CI",
    body: "The beachhead Minari can win first: GitLab teams running pipelines that flakiness already taxes.",
  },
];

const ICP = [
  {
    title: "Scaleups & platform teams",
    copy: "Fast-growing engineering orgs whose CI has become a daily bottleneck of red-but-not-broken builds.",
  },
  {
    title: "Developer-experience teams",
    copy: "DevEx and platform groups chartered to protect velocity. Flakiness is squarely their mandate.",
  },
  {
    title: "Open-source maintainers",
    copy: "Projects drowning in flaky-failure issues, where a verified auto-fix MR is an immediate relief.",
  },
];

export function Market() {
  return (
    <section id="market" className="relative z-10 overflow-hidden py-32" style={{ background: "#050505" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Target Market</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-5">
            Every team with CI
            <br />
            <span className="text-white/[0.48]">has flaky tests.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-12 max-w-3xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            Minari enters through GitLab-native teams who feel flakiness every day, expands across
            Git-based CI, and scales into the broader quality-tooling market. Figures are
            top-down estimates from public market reports.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 items-center gap-10 lg:grid-cols-2">
          {/* Pyramid: SOM apex, TAM base (Mirai-style triangle) */}
          <Reveal delay={2}>
            <div className="relative mx-auto flex min-h-[30rem] w-full max-w-[30rem] items-center justify-center">
              {/* Triangle body */}
              <div
                aria-hidden
                className="absolute bottom-3 max-w-full"
                style={{
                  width: "28rem",
                  height: "24rem",
                  clipPath: "polygon(50% 0%, 100% 100%, 0% 100%)",
                  background:
                    "linear-gradient(180deg, rgba(34,211,238,0.2) 0%, rgba(139,92,246,0.16) 58%, rgba(16,185,129,0.2) 100%)",
                  border: "1px solid rgba(161,161,170,0.42)",
                  boxShadow: "0 22px 80px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.12)",
                }}
              />

              {/* Tier divider lines */}
              <div className="absolute bottom-3 h-px max-w-[92%]" style={{ width: "22rem", background: "rgba(228,228,231,0.45)" }} />
              <div className="absolute h-px max-w-[66%]" style={{ bottom: "7.25rem", width: "16rem", background: "rgba(228,228,231,0.45)" }} />
              <div className="absolute h-px max-w-[40%]" style={{ bottom: "12rem", width: "9.25rem", background: "rgba(228,228,231,0.45)" }} />

              {/* Tier labels */}
              <div className="absolute left-1/2 -translate-x-1/2 text-center" style={{ bottom: "12.5rem" }}>
                <div className="text-[0.74rem] font-bold uppercase tracking-[0.14em] text-white/[0.92]">SOM</div>
                <div className="text-[1.55rem] font-bold tracking-[-0.04em] text-white">$120M</div>
              </div>
              <div className="absolute left-1/2 -translate-x-1/2 text-center" style={{ bottom: "7.7rem" }}>
                <div className="text-[0.74rem] font-bold uppercase tracking-[0.14em] text-white/[0.92]">SAM</div>
                <div className="text-[1.55rem] font-bold tracking-[-0.04em] text-white">$6B</div>
              </div>
              <div className="absolute left-1/2 -translate-x-1/2 text-center" style={{ bottom: "3rem" }}>
                <div className="text-[0.74rem] font-bold uppercase tracking-[0.14em] text-white/[0.92]">TAM</div>
                <div className="text-[1.55rem] font-bold tracking-[-0.04em] text-white">$48B</div>
              </div>

              {/* Floating tier dots (Mirai colors) */}
              <span
                className="absolute"
                style={{ top: "4.5rem", left: "48%", width: 10, height: 10, borderRadius: "9999px", background: "#67e8f9", boxShadow: "0 0 16px rgba(103,232,249,0.9)" }}
                aria-hidden
              />
              <span
                className="absolute"
                style={{ top: "9.5rem", left: "29%", width: 12, height: 12, borderRadius: "9999px", background: "#c4b5fd", boxShadow: "0 0 15px rgba(196,181,253,0.85)" }}
                aria-hidden
              />
              <span
                className="absolute"
                style={{ top: "14rem", left: "66%", width: 10, height: 10, borderRadius: "9999px", background: "#6ee7b7", boxShadow: "0 0 15px rgba(110,231,183,0.9)" }}
                aria-hidden
              />
            </div>
          </Reveal>

          {/* Segment detail */}
          <Reveal delay={3}>
            <div className="flex flex-col gap-6">
              {SEGMENTS.map((s) => (
                <div key={s.key} className="relative pl-5">
                  <span className="absolute bottom-1 left-0 top-1 w-[2px] rounded-full" style={{ background: s.color }} />
                  <div className="mb-1.5 flex items-baseline justify-between gap-4">
                    <span className="text-[0.8rem] font-bold uppercase tracking-[0.12em]" style={{ color: s.color }}>
                      {s.key}
                    </span>
                    <span className="text-[1.05rem] font-bold tracking-[-0.03em] text-white">{s.value}</span>
                  </div>
                  <div className="mb-1 text-[1rem] font-bold text-white">{s.title}</div>
                  <div className="text-[0.9rem] leading-relaxed text-white/[0.92]">{s.body}</div>
                </div>
              ))}
            </div>
          </Reveal>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
          {ICP.map((entry, i) => (
            <Reveal key={entry.title} delay={(i + 1) as 1 | 2 | 3}>
              <div className="glass-panel h-full rounded-2xl p-6 transition-colors duration-300 hover:border-white/30">
                <div className="mb-2 text-[1.02rem] font-bold text-white">{entry.title}</div>
                <div className="text-[0.9rem] leading-relaxed text-white/[0.92]">{entry.copy}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
