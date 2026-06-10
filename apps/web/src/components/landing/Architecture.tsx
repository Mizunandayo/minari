import { Network, Database, Plug, Server } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

const STAGES = ["Detect", "Diagnose", "Fix", "Verify", "Deliver"];

const SERVICES = [
  { icon: "/icons/gitlab.svg", name: "GitLab MCP", role: "Code · CI · MRs" },
  { icon: "/icons/gemini.svg", name: "Gemini 2.5", role: "Reasoning" },
  { icon: "/icons/supabase.svg", name: "Supabase", role: "Postgres · pgvector" },
  { icon: "/icons/redis.svg", name: "Upstash Redis", role: "Rate limits" },
];

const PILLARS = [
  {
    Icon: Network,
    title: "LangGraph agent swarm",
    desc: "Each stage is a node with a conditional edge. Low confidence ends the run early; a verified fix flows through to delivery.",
  },
  {
    Icon: Plug,
    title: "GitLab over MCP, both ways",
    desc: "Minari consumes the GitLab MCP server to read code and drive CI, and exposes itself as an MCP server so other agents can call detect, diagnose, fix and verify.",
  },
  {
    Icon: Database,
    title: "Supabase + pgvector",
    desc: "Tests, runs, diagnoses, fixes, verifications and merge requests persist in Postgres; HNSW vector search recalls similar past failures.",
  },
  {
    Icon: Server,
    title: "Cloud-native, resilient",
    desc: "FastAPI on Cloud Run (Tokyo), Next.js on Vercel, Upstash Redis for shared rate limits, with graceful degradation on every node.",
  },
];

function Connector({ label }: { label: string }) {
  return (
    <div className="flex flex-col items-center py-2" aria-hidden>
      <span className="h-5 w-px bg-white/20" />
      <span className="my-1 rounded-full border border-white/[0.12] bg-white/[0.03] px-3 py-0.5 text-[0.68rem] font-semibold tracking-[0.04em] text-white/[0.78]">
        {label}
      </span>
      <span className="h-5 w-px bg-white/20" />
    </div>
  );
}

function SystemDiagram() {
  return (
    <div className="glass-panel rounded-2xl p-6 sm:p-8">
      {/* Tier 1: interface */}
      <div className="mx-auto flex max-w-md items-center gap-3 rounded-xl border border-white/[0.14] bg-white/[0.03] px-5 py-3.5">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/icons/nextjs.svg" alt="" aria-hidden width={22} height={22} />
        <div>
          <div className="text-[0.66rem] font-bold uppercase tracking-[0.14em] text-white/[0.78]">Interface</div>
          <div className="text-[0.92rem] font-bold text-white">Next.js dashboard · live SSE stream</div>
        </div>
      </div>

      <Connector label="SSE / HTTPS · API-key + HMAC" />

      {/* Tier 2: agent core */}
      <div className="rounded-xl border border-white/[0.16] bg-white/[0.05] p-4">
        <div className="mb-3 flex items-center justify-center gap-2 text-[0.66rem] font-bold uppercase tracking-[0.14em] text-white/[0.78]">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/icons/fastapi.svg" alt="" aria-hidden width={16} height={16} />
          FastAPI · LangGraph agent
        </div>
        <div className="flex items-center justify-center gap-1.5 overflow-x-auto pb-1">
          {STAGES.map((s, i) => (
            <div key={s} className="flex items-center gap-1.5">
              <span className="whitespace-nowrap rounded-lg border border-white/25 bg-white/[0.05] px-3 py-2 text-[0.82rem] font-bold text-white">
                {s}
              </span>
              {i < STAGES.length - 1 && <span className="text-white/[0.48]" aria-hidden>→</span>}
            </div>
          ))}
        </div>
      </div>

      <Connector label="GitLab MCP · SQL · model calls" />

      {/* Tier 3: services */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {SERVICES.map((svc) => (
          <div
            key={svc.name}
            className="flex items-center gap-2.5 rounded-xl border border-white/[0.14] bg-white/[0.03] px-3.5 py-3"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={svc.icon} alt="" aria-hidden width={20} height={20} className="shrink-0" />
            <div className="min-w-0">
              <div className="truncate text-[0.88rem] font-bold text-white">{svc.name}</div>
              <div className="truncate text-[0.72rem] font-medium text-white/[0.78]">{svc.role}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Architecture() {
  return (
    <section id="architecture" className="relative z-10 py-32" style={{ background: "#070707" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Architecture</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-4">
            A pipeline of specialists,
            <br />
            <span className="text-white/[0.48]">not one monolithic prompt.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-12 max-w-2xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            Five agents, each with one job and one well-defined hand-off, orchestrated by
            LangGraph and grounded in real GitLab and Supabase data.
          </p>
        </Reveal>

        <Reveal delay={2}>
          <SystemDiagram />
        </Reveal>

        <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
          {PILLARS.map((p, i) => (
            <Reveal key={p.title} delay={((i % 2) + 1) as 1 | 2}>
              <div className="glass-panel flex h-full items-start gap-4 rounded-2xl p-6 transition-colors duration-300 hover:border-white/30">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-white/[0.18] bg-white/[0.03]">
                  <p.Icon size={19} strokeWidth={2} className="text-white" aria-hidden />
                </span>
                <div>
                  <div className="mb-1.5 text-[1rem] font-bold text-white">{p.title}</div>
                  <div className="text-[0.9rem] leading-relaxed text-white/[0.92]">{p.desc}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
