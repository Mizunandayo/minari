import { FlaskConical, Clock, EyeOff } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel } from "./Primitives";

const KPIS = [
  {
    Icon: FlaskConical,
    color: "var(--color-info)",
    n: "16%",
    u: "of tests",
    t: "Flakiness is universal at scale",
    d: "Google measured ~16% of its own tests as flaky. The best-resourced suite on earth still has them, and so does yours.",
  },
  {
    Icon: Clock,
    color: "var(--color-warn)",
    n: "5+",
    u: "hrs / dev / week",
    t: "Time lost chasing ghosts",
    d: "Engineers routinely lose several hours a week re-running pipelines and bisecting failures that were never actually bugs.",
  },
  {
    Icon: EyeOff,
    color: "var(--color-crit)",
    n: "0",
    u: "trust left",
    t: "The suite stops meaning anything",
    d: "After enough false alarms, teams reflexively ignore red, including the one failure that was a genuine break.",
  },
];

export function Problem() {
  return (
    <section id="problem" className="relative z-10 py-32" style={{ background: "#070707" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel center>Problem Statement</MicroLabel>
        </Reveal>

        <Reveal delay={1}>
          <h2
            className="mx-auto max-w-[42rem] text-center font-bold leading-[1.1] tracking-[-0.025em] text-white"
            style={{ fontSize: "clamp(1.9rem,4vw,3rem)" }}
          >
            Flaky tests don&apos;t fail because the code is wrong.
          </h2>
        </Reveal>

        <Reveal delay={2}>
          <p
            className="mx-auto mt-6 max-w-[40rem] text-center text-white/[0.92]"
            style={{ fontSize: "clamp(1.05rem,1.5vw,1.2rem)", lineHeight: 1.7 }}
          >
            They fail because timing, ordering, and shared state are unreliable, and that
            unreliability quietly erodes trust in the whole suite. Most tools can only point at
            them; fixing by hand is slow, and the lazy fix, weakening the test, is worse than the
            flake itself.
          </p>
        </Reveal>

        <div className="mt-16 grid grid-cols-1 gap-4 md:grid-cols-3">
          {KPIS.map((k, i) => (
            <Reveal key={k.t} delay={(i + 1) as 1 | 2 | 3}>
              <div className="glass-panel flex h-full flex-col rounded-2xl p-7 transition-colors duration-300 hover:border-white/30">
                <span
                  className="mb-6 flex h-11 w-11 items-center justify-center rounded-xl border"
                  style={{
                    borderColor: `color-mix(in srgb, ${k.color} 38%, transparent)`,
                    background: `color-mix(in srgb, ${k.color} 14%, transparent)`,
                  }}
                >
                  <k.Icon size={20} strokeWidth={2.2} style={{ color: k.color }} aria-hidden />
                </span>

                <div className="flex items-end gap-1.5">
                  <span className="font-bold tracking-[-0.04em] text-white" style={{ fontSize: "clamp(2.2rem,4vw,3rem)" }}>
                    {k.n}
                  </span>
                  <span className="mb-2 text-[0.95rem] font-semibold" style={{ color: k.color }}>
                    {k.u}
                  </span>
                </div>

                <div className="mt-2 text-[1.02rem] font-bold text-white">{k.t}</div>
                <div className="mt-2 text-[0.92rem] leading-relaxed text-white/[0.92]">{k.d}</div>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={3}>
          <p className="mt-6 text-center text-[0.8rem] text-white/[0.78]">
            Flakiness rate from Google&apos;s published testing research; other figures are
            representative of industry experience.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
