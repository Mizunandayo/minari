import Link from "next/link";
import { Play, ArrowRight } from "lucide-react";
import { Reveal } from "@/hooks/useScrollReveal";
import { MicroLabel, DisplayHeading } from "./Primitives";

export function Demo() {
  return (
    <section id="demo" className="relative z-10 py-32" style={{ background: "#050505" }}>
      <div className="mx-auto max-w-[1100px] px-8">
        <div className="mb-12 flex flex-col items-center text-center">
          <Reveal>
            <MicroLabel center>See It Run</MicroLabel>
          </Reveal>
          <Reveal delay={1}>
            <DisplayHeading className="text-center">
              Trigger a test.
              <br />
              <span className="text-white/[0.48]">Watch the whole repair.</span>
            </DisplayHeading>
          </Reveal>
        </div>

        <Reveal delay={2}>
          <div className="group relative overflow-hidden rounded-3xl border border-white/[0.14] bg-white/[0.03]">
            <div
              className="flex w-full items-center justify-center"
              style={{
                aspectRatio: "16 / 9",
                background:
                  "radial-gradient(ellipse 55% 60% at 50% 45%, rgba(255,255,255,0.05) 0%, transparent 70%), repeating-linear-gradient(135deg, rgba(255,255,255,0.02) 0 16px, transparent 16px 32px)",
              }}
            >
              <div className="flex flex-col items-center gap-4">
                <span className="flex h-20 w-20 items-center justify-center rounded-full border border-white/[0.18] bg-white/[0.06] transition-transform duration-300 group-hover:scale-105">
                  <Play size={30} strokeWidth={2} className="ml-1 text-white" aria-hidden />
                </span>
                <span className="text-[0.95rem] font-semibold text-white/[0.78]">
                  Three-minute demo · drop the recording here
                </span>
              </div>
            </div>
          </div>
        </Reveal>

        <Reveal delay={3}>
          <div className="mt-8 flex justify-center">
            <Link
              href="/dashboard"
              className="inline-flex cursor-pointer items-center gap-2.5 rounded-full bg-white px-7 py-3.5 text-[0.95rem] font-bold text-black transition-transform duration-150 hover:-translate-y-0.5"
            >
              Open the live dashboard
              <ArrowRight size={18} strokeWidth={2.4} aria-hidden />
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
