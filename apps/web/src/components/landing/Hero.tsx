"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { ArrowRight, GitBranch } from "lucide-react";

const PROOF = [
  { num: "5", lbl: "autonomous stages" },
  { num: "<2 min", lbl: "detect to delivery" },
  { num: "5×", lbl: "CI-verified" },
  { num: "0", lbl: "auto-merges" },
];

const META = [
  { label: "Developer", value: "Francis Daniel · Mizu" },
  { label: "Track", value: "GitLab · MCP" },
  { label: "Deadline", value: "Jun 12, 2026 · GMT+8" },
];

const BUILT_WITH = "Gemini 2.5 · LangGraph · GitLab MCP · Google Cloud Run";

/* Subtle randomized star-field behind the headline. */
function StarField() {
  const ref = useRef<HTMLCanvasElement | null>(null);
  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < 220; i++) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        const r = Math.random() * 1.1 + 0.15;
        const op = Math.random() * 0.5 + 0.08;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${op})`;
        ctx.fill();
      }
    };
    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      draw();
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    return () => ro.disconnect();
  }, []);
  return <canvas ref={ref} aria-hidden className="pointer-events-none absolute inset-0 z-0 h-full w-full" />;
}

export function Hero() {
  return (
    <section id="hero" className="relative min-h-[100dvh] overflow-hidden bg-[#050505]">
      <StarField />
      {/* Perspective grid, weighted toward the headline */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-0"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)",
          backgroundSize: "78px 78px",
          maskImage: "radial-gradient(ellipse 75% 65% at 30% 42%, black 25%, transparent 100%)",
          WebkitMaskImage: "radial-gradient(ellipse 75% 65% at 30% 42%, black 25%, transparent 100%)",
        }}
      />
      {/* Spotlight, pulled left to balance the left-aligned headline */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1]"
        style={{ background: "radial-gradient(ellipse 55% 55% at 28% 40%, rgba(255,255,255,0.06) 0%, transparent 70%)" }}
      />

      {/* Editorial left-aligned column */}
      <div className="relative z-[2] mx-auto flex min-h-[100dvh] max-w-5xl flex-col justify-center px-6 pb-16 pt-28">
        <p
          className="hero-enter mb-7 text-[0.78rem] font-semibold uppercase tracking-[0.2em] text-white/[0.78]"
          style={{ animationDelay: "0.05s" }}
        >
          Google Cloud Rapid Agent Hackathon · GitLab Track
        </p>

        <h1
          className="hero-enter flex flex-wrap items-baseline gap-x-5 font-bold leading-[0.88] tracking-[-0.04em] text-white"
          style={{ animationDelay: "0.14s", fontSize: "clamp(3.5rem,9vw,7rem)" }}
        >
          <span>Minari</span>
          <span className="font-semibold text-white/[0.5]" style={{ letterSpacing: "-0.02em" }}>
            実成
          </span>
        </h1>

        <p
          className="hero-enter mt-6 max-w-[40rem] text-white"
          style={{ animationDelay: "0.24s", fontSize: "clamp(1.3rem,2.6vw,2rem)", fontWeight: 600, letterSpacing: "-0.015em", lineHeight: 1.2 }}
        >
          Autonomous flaky-test intelligence. The agent that doesn&apos;t just flag a flaky test,
          it fixes one.
        </p>

        <p
          className="hero-enter mt-5 max-w-[37rem] text-white/[0.92]"
          style={{ animationDelay: "0.32s", fontSize: "clamp(1rem,1.4vw,1.12rem)", lineHeight: 1.7 }}
        >
          Detect → diagnose → fix → verify → deliver. Minari proves every fix in real GitLab CI and
          opens a reviewed merge request. It never weakens an assertion, and never merges on its own.
        </p>

        {/* CTAs */}
        <div className="hero-enter mt-9 flex flex-wrap items-center gap-3" style={{ animationDelay: "0.42s" }}>
          <Link
            href="/dashboard"
            aria-label="Watch a live diagnosis on the dashboard"
            className="inline-flex cursor-pointer items-center gap-2.5 rounded-full bg-white px-7 py-3.5 text-[0.95rem] font-bold text-black transition-transform duration-150 ease-out hover:-translate-y-0.5"
          >
            Watch a live diagnosis
            <ArrowRight size={18} strokeWidth={2.4} aria-hidden />
          </Link>
          <a
            href="https://github.com/Mizunandayo/minari"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View the Minari source on GitHub"
            className="inline-flex cursor-pointer items-center gap-2 rounded-full border border-white/[0.18] bg-white/[0.04] px-7 py-3.5 text-[0.95rem] font-semibold text-white/[0.92] backdrop-blur transition-colors duration-200 hover:border-white/40 hover:text-white"
          >
            <GitBranch size={17} strokeWidth={2} aria-hidden />
            View the repo
          </a>
        </div>

        {/* Inline proof ribbon: plain text, no box */}
        <div
          className="hero-enter mt-9 flex flex-wrap items-center gap-x-3.5 gap-y-2 text-[0.92rem] text-white/[0.92]"
          style={{ animationDelay: "0.5s" }}
        >
          {PROOF.map((p, i) => (
            <span key={p.lbl} className="flex items-center gap-3.5">
              <span>
                <span className="font-bold tracking-[-0.02em] text-white">{p.num}</span> {p.lbl}
              </span>
              {i < PROOF.length - 1 && <span className="text-white/[0.35]" aria-hidden>·</span>}
            </span>
          ))}
        </div>

        {/* Footer: identity + stack */}
        <div
          className="hero-enter mt-12 flex flex-wrap items-end justify-between gap-x-8 gap-y-6 border-t border-white/[0.1] pt-7"
          style={{ animationDelay: "0.58s" }}
        >
          <div className="flex flex-wrap gap-x-9 gap-y-4">
            {META.map((m) => (
              <div key={m.label} className="flex flex-col gap-1">
                <span className="text-[0.66rem] font-bold uppercase tracking-[0.14em] text-white/[0.78]">
                  {m.label}
                </span>
                <span className="text-[0.9rem] font-semibold text-white">{m.value}</span>
              </div>
            ))}
          </div>
          <p className="text-[0.8rem] font-medium text-white/[0.78]">
            Built with <span className="text-white">{BUILT_WITH}</span>
          </p>
        </div>
      </div>
    </section>
  );
}
