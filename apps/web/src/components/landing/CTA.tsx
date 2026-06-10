import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";

const FOOTER_LINKS = [
  { label: "Live App", href: "https://minari-eight.vercel.app" },
  { label: "API Health", href: "https://minari-api-1063669194601.asia-northeast1.run.app/api/v1/healthz" },
  { label: "Demo Repo", href: "https://gitlab.com/francisdanielgenese-group/francisdanielgenese-project" },
];

export function CTA() {
  return (
    <section className="relative z-10 overflow-hidden py-32" style={{ background: "#050505" }}>
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{ background: "radial-gradient(ellipse 60% 50% at 50% 100%, rgba(255,255,255,0.04) 0%, transparent 70%)" }}
      />
      <div className="relative z-10 mx-auto max-w-[1100px] px-8">
        <Reveal>
          <div className="relative mb-12 overflow-hidden rounded-3xl border border-white/[0.14] bg-white/[0.03] px-8 py-20 text-center sm:px-12">
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 rounded-3xl"
              style={{ background: "radial-gradient(ellipse 55% 40% at 50% 0%, rgba(255,255,255,0.1) 0%, transparent 70%)" }}
            />
            <div className="relative z-10">
              <p className="mb-6 text-[0.82rem] font-bold uppercase tracking-[0.14em] text-white/[0.78]">
                GitLab Track · Rapid Agent Hackathon · 2026
              </p>
              <h2
                className="mb-6 font-bold leading-[0.98] tracking-[-0.04em] text-white"
                style={{ fontSize: "clamp(2.6rem,7vw,5.5rem)" }}
              >
                Stop re-running.
                <br />
                Start trusting the suite.
              </h2>
              <p className="mx-auto mb-10 max-w-md text-[1rem] leading-relaxed text-white/[0.92]">
                Watch Minari diagnose a flaky test, prove the fix in real CI, and open a reviewed
                merge request, end to end, in under two minutes.
              </p>
              <div className="flex flex-wrap justify-center gap-3">
                <Link
                  href="/dashboard"
                  className="inline-flex cursor-pointer items-center gap-2 rounded-xl bg-white px-8 py-4 text-[0.95rem] font-bold text-black transition-transform duration-150 hover:-translate-y-0.5"
                >
                  Watch a live diagnosis
                  <ArrowRight size={18} strokeWidth={2.4} aria-hidden />
                </Link>
                <a
                  href="https://minari-eight.vercel.app"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex cursor-pointer items-center gap-2 rounded-xl border border-white/[0.18] bg-white/[0.04] px-8 py-4 text-[0.95rem] font-semibold text-white/[0.92] transition-colors duration-200 hover:border-white/40 hover:text-white"
                >
                  Open the live app
                </a>
              </div>
            </div>
          </div>
        </Reveal>

        <Reveal delay={1}>
          <footer className="flex flex-wrap items-center justify-between gap-4 border-t border-white/[0.14] pt-6">
            <span className="text-[0.9rem] font-bold uppercase tracking-[0.16em] text-white">
              実成 Minari
            </span>
            <span className="text-[0.85rem] font-medium text-white/[0.78]">
              Built by Francis Daniel Genese · GitLab Track · Rapid Agent Hackathon 2026
            </span>
            <div className="flex gap-5">
              {FOOTER_LINKS.map((l) => (
                <a
                  key={l.label}
                  href={l.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="cursor-pointer text-[0.82rem] font-semibold text-white/[0.78] transition-colors hover:text-white"
                >
                  {l.label}
                </a>
              ))}
            </div>
          </footer>
        </Reveal>
      </div>
    </section>
  );
}
