import Link from "next/link";
import { ArrowRight } from "lucide-react";
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
          <div className="relative overflow-hidden rounded-3xl border border-white/[0.14] bg-black">
            <iframe
              className="block w-full"
              style={{ aspectRatio: "16 / 9" }}
              src="https://www.youtube.com/embed/ndJ8cZIg4cM"
              title="Minari — three-minute demo"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
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
