"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

const LINKS = [
  { id: "problem", label: "Problem" },
  { id: "workflow", label: "Pipeline" },
  { id: "demo", label: "Demo" },
  { id: "architecture", label: "Architecture" },
  { id: "gemini", label: "Gemini" },
  { id: "features", label: "Features" },
  { id: "techstack", label: "Stack" },
  { id: "why-minari", label: "Why Minari" },
  { id: "market", label: "Market" },
  { id: "revenue", label: "Revenue" },
  { id: "roadmap", label: "Roadmap" },
];

export function LandingNav() {
  const [active, setActive] = useState("");

  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      { threshold: 0.3 },
    );
    document.querySelectorAll("section[id]").forEach((s) => obs.observe(s));
    return () => obs.disconnect();
  }, []);

  const go = (e: React.MouseEvent, id: string) => {
    e.preventDefault();
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <nav
      aria-label="Section navigation"
      className="nav-glass fixed left-1/2 top-5 z-50 flex h-[52px] -translate-x-1/2 items-center gap-0.5 rounded-full border border-white/[0.18] px-1.5 shadow-[0_0_0_1px_rgba(0,0,0,0.5),0_8px_32px_rgba(0,0,0,0.4)]"
      style={{ minWidth: "max-content" }}
    >
      <a
        href="#hero"
        onClick={(e) => go(e, "hero")}
        className="flex cursor-pointer items-center gap-2 px-4 text-[0.84rem] font-bold uppercase tracking-[0.14em] text-white"
        style={{ whiteSpace: "nowrap" }}
      >
        <span className="text-[0.96rem]" aria-hidden>
          実成
        </span>
        Minari
      </a>

      <span className="mx-1 h-5 w-px shrink-0 bg-white/10" aria-hidden />

      <div className="hidden items-center gap-0.5 lg:flex">
        {LINKS.map(({ id, label }) => (
          <a
            key={id}
            href={`#${id}`}
            onClick={(e) => go(e, id)}
            className={`cursor-pointer whitespace-nowrap rounded-full px-3 py-1.5 text-[0.84rem] transition-all duration-200 ${
              active === id
                ? "bg-white/[0.16] font-semibold text-white"
                : "font-medium text-white/[0.78] hover:text-white"
            }`}
          >
            {label}
          </a>
        ))}
      </div>

      <span className="mx-1 h-5 w-px shrink-0 bg-white/10" aria-hidden />

      <Link
        href="/dashboard"
        aria-label="Open the live dashboard"
        className="inline-flex cursor-pointer items-center gap-1.5 whitespace-nowrap rounded-full bg-white px-4 py-2 text-[0.8rem] font-bold text-black transition-transform duration-150 hover:-translate-y-0.5"
      >
        Live Dashboard
        <ArrowUpRight size={14} strokeWidth={2.6} aria-hidden />
      </Link>
    </nav>
  );
}
