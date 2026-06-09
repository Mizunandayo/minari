import { ShieldCheck, Repeat2, TrendingUp, Leaf, GitPullRequestArrow, Check } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

/* ---------- inline graphics (no screenshots needed) ---------- */

function GateChecks() {
  const rows = [
    { label: "Syntax valid", sub: "tree-sitter parse" },
    { label: "Assertions preserved", sub: "AST walk · original ⊆ fixed" },
    { label: "Assertions unmodified", sub: "DB-enforced constraint" },
  ];
  return (
    <div className="mt-5 flex flex-col gap-2">
      {rows.map((r) => (
        <div key={r.label} className="flex items-center gap-3 rounded-xl border border-white/[0.1] bg-white/[0.02] px-4 py-2.5">
          <span
            className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
            style={{ background: "color-mix(in srgb, var(--color-pass) 18%, transparent)" }}
          >
            <Check size={13} strokeWidth={3.2} style={{ color: "var(--color-pass)" }} aria-hidden />
          </span>
          <span className="flex flex-1 items-center justify-between gap-3">
            <span className="text-[0.9rem] font-semibold text-white">{r.label}</span>
            <span className="font-mono text-[0.72rem] text-white/[0.78]">{r.sub}</span>
          </span>
        </div>
      ))}
    </div>
  );
}

function VerifyRuns() {
  return (
    <div className="mt-2">
      <div className="flex items-end gap-2">
        {[1, 2, 3, 4, 5].map((n) => (
          <div key={n} className="flex flex-1 flex-col items-center gap-2">
            <div
              className="flex w-full items-center justify-center rounded-md"
              style={{
                height: 46,
                background: "color-mix(in srgb, var(--color-pass) 15%, transparent)",
                border: "1px solid color-mix(in srgb, var(--color-pass) 40%, transparent)",
              }}
            >
              <Check size={16} strokeWidth={3} style={{ color: "var(--color-pass)" }} aria-hidden />
            </div>
            <span className="text-[0.7rem] font-semibold text-white/[0.78]">Run {n}</span>
          </div>
        ))}
      </div>
      {/* variance reduction bar */}
      <div className="mt-5">
        <div className="mb-1.5 flex items-center justify-between text-[0.8rem] font-semibold">
          <span className="text-white/[0.78]">Variance reduction</span>
          <span style={{ color: "var(--color-pass)" }}>↓ 87%</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-white/[0.06]">
          <div className="h-full rounded-full" style={{ width: "87%", background: "var(--color-pass)" }} />
        </div>
      </div>
    </div>
  );
}

function ConfidenceCascade() {
  const seg = [
    { k: "Detect", c: "var(--color-info)" },
    { k: "Diagnose", c: "var(--color-info)" },
    { k: "Fix", c: "var(--color-warn)" },
    { k: "Pass-rate", c: "var(--color-pass)" },
  ];
  return (
    <div className="mt-4">
      <div className="flex gap-1.5">
        {seg.map((s) => (
          <div key={s.k} className="h-2 flex-1 rounded-full" style={{ background: s.c, opacity: 0.85 }} title={s.k} />
        ))}
      </div>
      <div className="mt-2 flex items-baseline gap-1.5">
        <span className="text-[1.6rem] font-bold tracking-[-0.04em] text-white">92%</span>
        <span className="text-[0.78rem] font-medium text-white/[0.78]">overall confidence</span>
      </div>
    </div>
  );
}

function ForecastSpark() {
  // declining flakiness sparkline
  const pts = [4, 18, 30, 22, 26, 16, 12, 9, 6, 4];
  const w = 160;
  const h = 40;
  const max = Math.max(...pts);
  const d = pts
    .map((p, i) => `${(i / (pts.length - 1)) * w},${h - (p / max) * (h - 4) - 2}`)
    .join(" ");
  return (
    <div className="mt-4">
      <svg viewBox={`0 0 ${w} ${h}`} className="h-10 w-full" preserveAspectRatio="none" aria-hidden>
        <polyline points={d} fill="none" stroke="var(--color-warn)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div className="mt-2 flex items-baseline gap-1.5">
        <span className="text-[1.05rem] font-bold text-white">7-day risk</span>
        <span className="text-[0.78rem] font-medium" style={{ color: "var(--color-pass)" }}>trending down</span>
      </div>
    </div>
  );
}

function CarbonStat() {
  return (
    <div className="mt-4 flex items-baseline gap-2">
      <span className="text-[1.9rem] font-bold tracking-[-0.05em]" style={{ color: "var(--color-pass)" }}>
        1.02 kg
      </span>
      <span className="text-[0.8rem] font-medium text-white/[0.78]">CO₂e avoided</span>
    </div>
  );
}

function ReasoningStream() {
  const lines: { dot: string; tag: string; text: string }[] = [
    { dot: "var(--color-info)", tag: "mcp", text: "get_file_contents · test_async_timing.py" },
    { dot: "var(--color-info)", tag: "reason", text: "race: result read before sleep settles" },
    { dot: "var(--color-warn)", tag: "fix", text: "candidate #1 · await-until-ready" },
    { dot: "var(--color-pass)", tag: "verify", text: "5/5 passed · gate PASSED" },
  ];
  return (
    <div className="mt-5 rounded-xl border border-white/[0.1] bg-[#050505] p-4 font-mono text-[0.78rem] leading-6">
      {lines.map((l) => (
        <div key={l.tag} className="flex items-center gap-2.5">
          <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: l.dot }} />
          <span className="shrink-0 uppercase tracking-[0.06em] text-white/[0.78]">{l.tag}</span>
          <span className="truncate text-white/[0.92]">{l.text}</span>
        </div>
      ))}
      <div className="mt-1 flex items-center gap-2.5">
        <span className="h-2 w-2 shrink-0 rounded-full bg-white/30" />
        <span className="badge-dot inline-block h-3.5 w-1.5" style={{ background: "var(--color-pass)" }} aria-hidden />
      </div>
    </div>
  );
}

const SMALL = [
  { Icon: TrendingUp, tag: "Confidence cascade", title: "One honest number", desc: "Detection × diagnosis × fix × pass-rate, multiplied into a single confidence on every MR.", graphic: <ConfidenceCascade /> },
  { Icon: TrendingUp, tag: "Predictive forecast", title: "Seven days ahead", desc: "An explainable trend model projects each test's flakiness before it breaks the build.", graphic: <ForecastSpark /> },
  { Icon: Leaf, tag: "Sustainability", title: "Quantified waste", desc: "Every avoided flaky re-run counted as saved CI compute, CO₂e, and engineer hours.", graphic: <CarbonStat /> },
];

export function Features() {
  return (
    <section id="features" className="relative z-10 overflow-hidden py-32" style={{ background: "#050505" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Features</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-14">Built to be trusted.</DisplayHeading>
        </Reveal>

        {/* Row 1: assertion safety (wide) + 5x verify */}
        <div className="mb-3 grid grid-cols-1 gap-3 lg:grid-cols-[7fr_5fr]">
          <Reveal delay={1}>
            <div className="glass-panel h-full rounded-2xl p-7 transition-colors duration-300 hover:border-white/30">
              <span
                className="mb-5 flex h-10 w-10 items-center justify-center rounded-xl border"
                style={{ borderColor: "color-mix(in srgb, var(--color-pass) 35%, transparent)", background: "color-mix(in srgb, var(--color-pass) 14%, transparent)" }}
              >
                <ShieldCheck size={18} strokeWidth={2.2} style={{ color: "var(--color-pass)" }} aria-hidden />
              </span>
              <span className="mb-2 block text-[0.82rem] font-bold uppercase tracking-[0.1em]" style={{ color: "var(--color-pass)" }}>
                Assertion-safety gate
              </span>
              <div className="mb-2 text-[1rem] font-bold text-white">
                Minari fixes the cause — it never weakens the test to force a pass.
              </div>
              <p className="text-[0.92rem] leading-relaxed text-white/[0.92]">
                An AST walk proves every original assertion still exists in the fix. The rule is
                even enforced in the database, so a fix that edits an assertion can&apos;t be stored.
              </p>
              <div className="mt-5 rounded-xl border border-white/[0.14] p-4 font-mono text-[0.82rem] leading-7" style={{ background: "#050505" }}>
                <span className="text-white/[0.78]">{"// fix adds synchronization — assertions untouched"}</span>
                <br />
                <span style={{ color: "var(--color-pass)" }}>+ await until(ready, timeout=2s)</span>
                <br />
                <span className="text-white/[0.92]">  assert result == expected</span>
              </div>
              <GateChecks />
            </div>
          </Reveal>

          <Reveal delay={2}>
            <div className="glass-panel h-full rounded-2xl p-7 transition-colors duration-300 hover:border-white/30">
              <span
                className="mb-5 flex h-10 w-10 items-center justify-center rounded-xl border"
                style={{ borderColor: "color-mix(in srgb, var(--color-info) 35%, transparent)", background: "color-mix(in srgb, var(--color-info) 14%, transparent)" }}
              >
                <Repeat2 size={18} strokeWidth={2.2} style={{ color: "var(--color-info)" }} aria-hidden />
              </span>
              <span className="mb-2 block text-[0.82rem] font-bold uppercase tracking-[0.1em]" style={{ color: "var(--color-info)" }}>
                Real verification
              </span>
              <div className="mb-2 text-[1rem] font-bold text-white">Proven in real CI, five times.</div>
              <p className="mb-2 text-[0.92rem] leading-relaxed text-white/[0.92]">
                The fix runs in a fresh pipeline five times; the gate demands 5/5 green plus a real
                drop in run-to-run variance before it ships.
              </p>
              <VerifyRuns />
            </div>
          </Reveal>
        </div>

        {/* Row 2: three small cards with mini-visuals */}
        <div className="mb-3 grid grid-cols-1 gap-3 md:grid-cols-3">
          {SMALL.map((c, i) => (
            <Reveal key={c.tag} delay={(i + 1) as 1 | 2 | 3}>
              <div className="glass-panel flex h-full flex-col rounded-2xl p-6 transition-colors duration-300 hover:border-white/30">
                <span className="mb-1.5 block text-[0.82rem] font-bold uppercase tracking-[0.1em] text-white/[0.78]">
                  {c.tag}
                </span>
                <div className="mb-1.5 text-[0.95rem] font-bold text-white">{c.title}</div>
                <div className="text-[0.88rem] leading-relaxed text-white/[0.92]">{c.desc}</div>
                {c.graphic}
              </div>
            </Reveal>
          ))}
        </div>

        {/* Row 3: human boundary + live reasoning */}
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          <Reveal delay={1}>
            <div className="glass-panel h-full rounded-2xl p-7 transition-colors duration-300 hover:border-white/30">
              <span className="mb-4 flex h-9 w-9 items-center justify-center rounded-xl border border-white/[0.18] bg-white/[0.03]">
                <GitPullRequestArrow size={17} strokeWidth={2.2} className="text-white" aria-hidden />
              </span>
              <span className="mb-2 block text-[0.82rem] font-bold uppercase tracking-[0.1em] text-white/[0.78]">
                Human boundary
              </span>
              <div className="mb-2 text-[0.96rem] font-bold text-white">It proposes. You decide.</div>
              <p className="text-[0.9rem] leading-relaxed text-white/[0.92]">
                Minari opens a merge request with a senior-engineer write-up and a reviewer — and
                never merges on its own. The final call always belongs to a person.
              </p>
            </div>
          </Reveal>
          <Reveal delay={2}>
            <div className="glass-panel h-full rounded-2xl p-7 transition-colors duration-300 hover:border-white/30">
              <span className="mb-2 block text-[0.82rem] font-bold uppercase tracking-[0.1em] text-white/[0.78]">
                Live reasoning
              </span>
              <div className="mb-2 text-[0.96rem] font-bold text-white">Watch it think, not a black box.</div>
              <p className="text-[0.9rem] leading-relaxed text-white/[0.92]">
                Every MCP call, decision, and fix candidate streams to the dashboard in real time.
              </p>
              <ReasoningStream />
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
