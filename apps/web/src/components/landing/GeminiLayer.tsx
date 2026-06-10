import { Sparkles, Braces, ShieldAlert, RefreshCw } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const MODELS = [
  {
    badge: "Diagnosis",
    name: "gemini-2.5-pro",
    use: "Deep root-cause reasoning on the uncertain cases (PFS 40–75).",
    points: [
      "Structured output → typed Diagnosis schema",
      "Reasoning chain streamed live to the panel",
      "Adaptive router escalates only when needed",
    ],
    color: "var(--color-info)",
  },
  {
    badge: "Repair",
    name: "gemini-2.5-flash",
    use: "Fast generation of three ranked fix candidates (~8s).",
    points: [
      "Confidence-ranked, never edits assertions",
      "Each candidate passes a tree-sitter syntax gate",
      "Flash keeps the loop interactive on stage",
    ],
    color: "var(--color-warn)",
  },
  {
    badge: "Memory",
    name: "gemini-embedding-001",
    use: "768-dim embeddings power similar-failure recall.",
    points: [
      "pgvector HNSW similarity search",
      "Surfaces past diagnoses of look-alike flakes",
      "Grounds the model in real prior evidence",
    ],
    color: "var(--color-pass)",
  },
];

const USES = [
  { Icon: Braces, title: "Structured output", desc: "Every model call returns a typed Pydantic schema, never free text the pipeline has to guess at." },
  { Icon: RefreshCw, title: "Self-repair loop", desc: "If the model returns a malformed schema, Minari re-prompts with the validation error until it parses." },
  { Icon: ShieldAlert, title: "Untrusted-data fencing", desc: "Test source and logs are fenced as untrusted input, so a crafted test can't hijack the prompt." },
  { Icon: Sparkles, title: "Adaptive routing", desc: "Pro for the genuinely uncertain diagnoses, Flash for everything else: accuracy where it matters, speed elsewhere." },
];

export function GeminiLayer() {
  return (
    <section id="gemini" className="relative z-10 overflow-hidden py-32" style={{ background: "#050505" }}>
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{ background: "radial-gradient(ellipse 60% 50% at 50% 0%, rgba(96,165,250,0.06) 0%, transparent 70%)" }}
      />
      <div className="relative z-10 mx-auto max-w-[1100px] px-8">
        <div className="mb-14 flex flex-col items-center gap-5">
          <Reveal>
            <span
              className="inline-flex h-16 w-16 items-center justify-center rounded-2xl border border-white/[0.18]"
              style={{ background: "rgba(96,165,250,0.1)" }}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/icons/gemini.svg" alt="Gemini" width={36} height={36} />
            </span>
          </Reveal>
          <Reveal delay={1}>
            <MicroLabel center>LLM Integration</MicroLabel>
          </Reveal>
          <Reveal delay={1}>
            <DisplayHeading className="text-center">
              Gemini is the
              <br />
              <span className="text-white/[0.5]">reasoning layer.</span>
            </DisplayHeading>
          </Reveal>
          <Reveal delay={2}>
            <p className="mx-auto max-w-xl text-center text-[1.03rem] leading-relaxed text-white/[0.92]">
              Diagnosis, repair, and recall all flow through Gemini 2.5. Deterministic gates
              (syntax, assertions, real CI) own the safety. The model reasons; the pipeline verifies.
            </p>
          </Reveal>
        </div>

        <div className="mb-3 grid grid-cols-1 gap-3 md:grid-cols-3">
          {MODELS.map((m, i) => (
            <Reveal key={m.name} delay={(i + 1) as 1 | 2 | 3}>
              <div className="glass-panel h-full overflow-hidden rounded-2xl transition-colors duration-300 hover:border-white/30">
                <div className="border-b border-white/[0.14] p-4" style={{ background: "rgba(255,255,255,0.02)" }}>
                  <div className="mb-2 text-[0.78rem] font-bold uppercase tracking-[0.1em]" style={{ color: m.color }}>
                    {m.badge}
                  </div>
                  <div className="font-mono text-[1rem] font-bold tracking-tight text-white">{m.name}</div>
                </div>
                <div className="p-4">
                  <p className="mb-4 text-[0.88rem] leading-relaxed text-white/[0.92]">{m.use}</p>
                  <div className="flex flex-col gap-2">
                    {m.points.map((p) => (
                      <div key={p} className="flex items-start gap-2 text-[0.85rem] leading-relaxed text-white/[0.92]">
                        <span className="mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full" style={{ background: m.color }} />
                        {p}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {USES.map((u, i) => (
            <Reveal key={u.title} delay={((i % 2) + 1) as 1 | 2}>
              <div className="glass-panel flex items-start gap-4 rounded-2xl p-5 transition-colors duration-300 hover:border-white/30">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/[0.18]" style={{ background: "rgba(255,255,255,0.03)" }}>
                  <u.Icon size={17} strokeWidth={2} className="text-white" aria-hidden />
                </span>
                <div>
                  <div className="mb-1 text-[0.96rem] font-bold text-white">{u.title}</div>
                  <div className="text-[0.88rem] leading-relaxed text-white/[0.92]">{u.desc}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
