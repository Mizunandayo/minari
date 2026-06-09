"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { ArrowRight, GitBranch } from "lucide-react";

const STATS = [
  { num: "5", lbl: "Autonomous stages" },
  { num: "<2 min", lbl: "Detect to delivery" },
  { num: "5×", lbl: "CI re-verification" },
  { num: "0", lbl: "Auto-merges" },
];

const META = [
  { label: "Developer", value: "Francis Daniel — Mizu" },
  { label: "Timeline", value: "May 06 – Jul 14, 2026" },
];

const SCHEDULE = [
  { phase: "Submissions", when: "May 6 – Jun 12" },
  { phase: "Judging", when: "Jun 23 – Jul 7" },
  { phase: "Winners", when: "Jul 14" },
];

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

  return (
    <canvas
      ref={ref}
      aria-hidden
      className="pointer-events-none absolute inset-0 z-0 h-full w-full"
    />
  );
}

export function Hero() {
  return (
    <section id="hero" className="relative min-h-[100dvh] overflow-hidden bg-[#050505]">
      <StarField />
      {/* Perspective grid */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-0"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)",
          backgroundSize: "80px 80px",
          maskImage: "radial-gradient(ellipse 70% 60% at 50% 50%, black 30%, transparent 100%)",
          WebkitMaskImage:
            "radial-gradient(ellipse 70% 60% at 50% 50%, black 30%, transparent 100%)",
        }}
      />
      {/* Spotlight */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1]"
        style={{
          background:
            "radial-gradient(ellipse 65% 55% at 50% 42%, rgba(255,255,255,0.055) 0%, transparent 70%)",
        }}
      />

      <div className="relative z-[2] flex min-h-[100dvh] flex-col items-center justify-center px-6 pb-20 pt-28 text-center">
        {/* Eyebrow — plain tracked text, no badge */}
        <p
          className="hero-enter mb-7 text-[0.8rem] font-semibold uppercase tracking-[0.22em] text-white/[0.78]"
          style={{ animationDelay: "0.05s" }}
        >
          Security &amp; Compliance + AI/ML API Track
        </p>

        {/* Wordmark */}
        <h1
          className="hero-enter flex flex-wrap items-baseline justify-center gap-x-5 font-bold leading-[0.9] tracking-[-0.035em] text-white"
          style={{ animationDelay: "0.16s", fontSize: "clamp(3.5rem,11vw,8rem)" }}
        >
          <span>Minari</span>
          <span className="font-semibold text-white/[0.5]" style={{ letterSpacing: "-0.02em" }}>
            実成
          </span>
        </h1>

        {/* Value line */}
        <p
          className="hero-enter mt-6 text-white"
          style={{ animationDelay: "0.26s", fontSize: "clamp(1.15rem,2.4vw,1.6rem)", fontWeight: 600, letterSpacing: "-0.01em" }}
        >
          Autonomous flaky-test intelligence.
        </p>

        {/* Supporting sentence */}
        <p
          className="hero-enter mt-4 max-w-[38rem] text-white/[0.92]"
          style={{ animationDelay: "0.34s", fontSize: "clamp(1rem,1.55vw,1.15rem)", lineHeight: 1.7 }}
        >
          Detect → diagnose → fix → verify → deliver. Minari repairs a flaky test end to end and
          opens a reviewed merge request — never weakening an assertion, never merging on its own.
        </p>

        {/* CTAs */}
        <div
          className="hero-enter mt-10 flex flex-wrap items-center justify-center gap-3"
          style={{ animationDelay: "0.44s" }}
        >
          <Link
            href="/dashboard"
            aria-label="Watch a live diagnosis on the dashboard"
            className="inline-flex cursor-pointer items-center gap-2.5 rounded-full bg-white px-7 py-3.5 text-[0.95rem] font-bold text-black transition-transform duration-150 ease-out hover:-translate-y-0.5"
          >
            Watch a live diagnosis
            <ArrowRight size={18} strokeWidth={2.4} aria-hidden />
          </Link>
          <a
            href="https://gitlab.com/francisdanielgenese-group/francisdanielgenese-project"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View the demo GitLab project"
            className="inline-flex cursor-pointer items-center gap-2 rounded-full border border-white/[0.18] bg-white/[0.04] px-7 py-3.5 text-[0.95rem] font-semibold text-white/[0.92] backdrop-blur transition-colors duration-200 hover:border-white/40 hover:text-white"
          >
            <GitBranch size={17} strokeWidth={2} aria-hidden />
            View the repo
          </a>
        </div>

        {/* Borderless live status (not a pill) */}
        <div
          className="hero-enter mt-7 flex items-center gap-2.5 text-[0.85rem] font-medium text-white/[0.78]"
          style={{ animationDelay: "0.52s" }}
        >
          <span
            className="badge-dot h-2 w-2 shrink-0 rounded-full"
            style={{ background: "var(--color-pass)" }}
            aria-hidden
          />
          Live on Cloud Run + Vercel · GitLab-native
        </div>

        {/* Stat bar — real proof */}
        <div
          className="hero-enter mt-11 grid w-full max-w-[600px] grid-cols-2 overflow-hidden rounded-2xl border border-white/[0.14] bg-white/[0.04] backdrop-blur sm:grid-cols-4"
          style={{ animationDelay: "0.6s" }}
        >
          {STATS.map((s, i) => (
            <div
              key={s.lbl}
              className={`flex flex-col items-center px-5 py-[18px] ${
                i !== 0 ? "border-white/[0.08] sm:border-l" : ""
              }`}
            >
              <span
                className="text-white"
                style={{ fontSize: "clamp(1.3rem,2.4vw,1.6rem)", fontWeight: 700, letterSpacing: "-0.04em" }}
              >
                {s.num}
              </span>
              <span className="mt-1 text-center text-[0.8rem] font-medium text-white/[0.78]">
                {s.lbl}
              </span>
            </div>
          ))}
        </div>

        {/* Developer + timeline */}
        <div
          className="hero-enter mt-10 flex flex-wrap items-start justify-center gap-x-12 gap-y-5"
          style={{ animationDelay: "0.68s" }}
        >
          {META.map((m) => (
            <div key={m.label} className="flex flex-col items-center gap-1">
              <span className="text-[0.72rem] font-bold uppercase tracking-[0.16em] text-white/[0.78]">
                {m.label}
              </span>
              <span className="text-[0.95rem] font-semibold text-white">{m.value}</span>
            </div>
          ))}
        </div>

        {/* Schedule timeline (GMT+8) */}
        <div
          className="hero-enter mt-5 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-[0.8rem] font-medium text-white/[0.78]"
          style={{ animationDelay: "0.74s" }}
        >
          {SCHEDULE.map((s, i) => (
            <span key={s.phase} className="flex items-center gap-4">
              <span>
                {s.phase} <span className="text-white">{s.when}</span>
              </span>
              {i < SCHEDULE.length - 1 && <span className="text-white/[0.4]" aria-hidden>·</span>}
            </span>
          ))}
          <span className="text-white/[0.4]" aria-hidden>·</span>
          <span>GMT+8</span>
        </div>
      </div>

      {/* Scroll cue */}
      <div className="relative z-[2] flex flex-col items-center gap-1.5 pb-6 opacity-30">
        <span className="h-8 w-px bg-white/50" />
        <span className="text-[0.78rem] font-semibold uppercase tracking-[0.16em] text-white/[0.78]">
          Scroll
        </span>
      </div>
    </section>
  );
}
