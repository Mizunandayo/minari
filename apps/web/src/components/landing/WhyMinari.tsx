import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";
import { CompetitorMatrix } from "@/components/dashboard/CompetitorMatrix";

export function WhyMinari() {
  return (
    <section id="why-minari" className="relative z-10 py-32" style={{ background: "#070707" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <Reveal>
          <MicroLabel>Why Minari</MicroLabel>
        </Reveal>
        <Reveal delay={1}>
          <DisplayHeading className="mb-4">
            Others detect.
            <br />
            <span className="text-white/[0.48]">Minari completes the loop.</span>
          </DisplayHeading>
        </Reveal>
        <Reveal delay={2}>
          <p className="mb-8 max-w-2xl text-[1.03rem] leading-relaxed text-white/[0.92]">
            These are the tools teams reach for today. Most stop at detecting or quarantining a
            flaky test. Minari is the only one that carries it all the way to a verified, reviewed
            merge request.
          </p>
        </Reveal>

        {/* Legend */}
        <Reveal delay={2}>
          <div className="mb-5 flex flex-wrap items-center gap-x-6 gap-y-2">
            <span className="flex items-center gap-2 text-[0.82rem] font-medium text-white/[0.92]">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-pass)" }} /> Does it
            </span>
            <span className="flex items-center gap-2 text-[0.82rem] font-medium text-white/[0.92]">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-warn)" }} /> Partial
            </span>
            <span className="flex items-center gap-2 text-[0.82rem] font-medium text-white/[0.92]">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--color-crit)" }} /> No
            </span>
          </div>
        </Reveal>

        {/* Full capability matrix — reuses the dashboard component so the two never drift */}
        <Reveal delay={2}>
          <CompetitorMatrix />
        </Reveal>

        <Reveal delay={3}>
          <Link
            href="/dashboard"
            className="mt-8 inline-flex cursor-pointer items-center gap-2 text-[0.95rem] font-semibold text-white/[0.92] transition-colors hover:text-white"
          >
            Open the live dashboard
            <ArrowRight size={17} strokeWidth={2.4} aria-hidden />
          </Link>
        </Reveal>

        <Reveal delay={3}>
          <p className="mt-6 text-[0.8rem] leading-relaxed text-white/[0.78]">
            Positioning reflects each product&apos;s publicly documented scope as of 2026 and is
            meant to show category boundaries, not to disparage any tool.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
