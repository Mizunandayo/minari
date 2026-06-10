import type { LucideIcon } from "lucide-react";
import {
  Workflow, Gauge, ScrollText, Package, ListTree, Languages, ShieldCheck,
  Boxes, Plug, ChartArea, Code2, KeySquare, Fingerprint, Waypoints, Radio,
} from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

// brand → Simple Icons slug (rendered white for the monochrome system);
// Icon → lucide fallback for tools without a brand mark.
type Item = { name: string; role: string; brand?: string; Icon?: LucideIcon };
type Layer = { cat: string; items: Item[] };

const LAYERS: Layer[] = [
  {
    cat: "Agent & LLM",
    items: [
      { name: "LangGraph", role: "Agent orchestration", brand: "langchain" },
      { name: "Gemini 2.5 Pro", role: "Diagnosis reasoning", brand: "gemini" },
      { name: "Gemini 2.5 Flash", role: "Fix generation", brand: "gemini" },
      { name: "gemini-embedding-001", role: "768-d embeddings", brand: "gemini" },
      { name: "MCP adapters", role: "Agent ↔ MCP bridge", Icon: Workflow },
    ],
  },
  {
    cat: "Backend",
    items: [
      { name: "Python 3.12", role: "Runtime", brand: "python" },
      { name: "FastAPI", role: "Async API", brand: "fastapi" },
      { name: "Pydantic v2", role: "Typed schemas", brand: "pydantic" },
      { name: "asyncpg", role: "Postgres driver", brand: "postgresql" },
      { name: "slowapi", role: "Rate limiting", Icon: Gauge },
      { name: "structlog", role: "Structured logs", Icon: ScrollText },
      { name: "sse-starlette", role: "Live SSE stream", Icon: Radio },
      { name: "uv", role: "Packaging", Icon: Package },
    ],
  },
  {
    cat: "Code analysis",
    items: [
      { name: "tree-sitter", role: "Syntax gate", Icon: ListTree },
      { name: "language-pack", role: "Multi-language parsers", Icon: Languages },
      { name: "defusedxml", role: "XXE-hardened JUnit", Icon: ShieldCheck },
    ],
  },
  {
    cat: "Data",
    items: [
      { name: "Supabase Postgres", role: "Primary store", brand: "supabase" },
      { name: "pgvector (HNSW)", role: "Similarity search", Icon: Boxes },
      { name: "Upstash Redis", role: "Shared rate-limit store", brand: "redis" },
    ],
  },
  {
    cat: "Integration",
    items: [
      { name: "GitLab MCP", role: "Reads, CI, merge requests", brand: "gitlab" },
      { name: "MCP server", role: "Minari exposed as tools", Icon: Plug },
    ],
  },
  {
    cat: "Frontend",
    items: [
      { name: "Next.js 16", role: "App Router", brand: "nextjs" },
      { name: "React 19", role: "UI runtime", brand: "react" },
      { name: "TypeScript", role: "Type safety", brand: "typescript" },
      { name: "Tailwind CSS v4", role: "Design tokens", brand: "tailwindcss" },
      { name: "Recharts", role: "Trend & forecast charts", Icon: ChartArea },
      { name: "Framer Motion", role: "Animation", brand: "framermotion" },
      { name: "lucide-react", role: "Icons", brand: "lucide" },
      { name: "prism", role: "Diff highlighting", Icon: Code2 },
    ],
  },
  {
    cat: "Infra & security",
    items: [
      { name: "Google Cloud Run", role: "API host (Tokyo)", brand: "googlecloud" },
      { name: "Vercel", role: "Frontend host", brand: "vercel" },
      { name: "Docker", role: "Python 3.12 + Node 20", brand: "docker" },
      { name: "Secret Manager", role: "Secrets at rest", Icon: KeySquare },
      { name: "Constant-time key", role: "HMAC API auth", Icon: Fingerprint },
      { name: "Stream tokens", role: "Per-run SSE auth", Icon: Waypoints },
      { name: "CSP + headers", role: "Hardened responses", Icon: ShieldCheck },
    ],
  },
];

function TechIcon({ brand, Icon }: { brand?: string; Icon?: LucideIcon }) {
  if (brand) {
    // Brand logos vendored locally in /public/icons (no runtime CDN dependency).
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img src={`/icons/${brand}.svg`} alt="" aria-hidden width={18} height={18} />
    );
  }
  if (Icon) return <Icon size={18} strokeWidth={2} className="text-white" aria-hidden />;
  return null;
}

export function TechStack() {
  return (
    <section id="techstack" className="relative z-10 py-32" style={{ background: "#050505" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Tech Stack</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-4">Every layer, in production.</DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-12 max-w-2xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            The full stack behind Minari: agent, backend, data, integration, frontend, and the
            security boundaries that make autonomous test repair safe to run.
          </p>
        </Reveal>

        <Reveal delay={2}>
          <div className="border-t border-white/[0.14]">
            {LAYERS.map((layer) => (
              <div
                key={layer.cat}
                className="grid grid-cols-1 gap-5 border-b border-white/[0.1] py-6 md:grid-cols-[180px_1fr]"
              >
                <div className="pt-1 text-[0.82rem] font-bold uppercase tracking-[0.1em] text-white/[0.78]">
                  {layer.cat}
                </div>
                <div className="flex flex-wrap gap-2.5">
                  {layer.items.map((it) => (
                    <div
                      key={it.name}
                      className="flex items-center gap-2.5 rounded-[10px] border border-white/[0.18] bg-white/[0.02] px-3 py-2 transition-colors duration-200 hover:border-white/35"
                    >
                      <span className="flex h-[18px] w-[18px] shrink-0 items-center justify-center">
                        <TechIcon brand={it.brand} Icon={it.Icon} />
                      </span>
                      <span className="flex flex-col gap-0.5 leading-tight">
                        <span className="text-[0.68rem] font-semibold uppercase tracking-[0.08em] text-white/[0.78]">
                          {it.role}
                        </span>
                        <span className="text-[0.92rem] font-bold tracking-[-0.01em] text-white">
                          {it.name}
                        </span>
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
