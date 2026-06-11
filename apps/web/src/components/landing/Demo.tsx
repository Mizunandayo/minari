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
          <a
            href="https://www.youtube.com/watch?v=ndJ8cZIg4cM"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Watch the Minari three-minute demo on YouTube"
            className="group relative block cursor-pointer overflow-hidden rounded-3xl border border-white/[0.14] bg-black"
          >
            <div
              className="flex w-full items-center justify-center bg-cover bg-center"
              style={{
                aspectRatio: "16 / 9",
                backgroundImage:
                  "linear-gradient(rgba(0,0,0,0.20), rgba(0,0,0,0.45)), url('https://img.youtube.com/vi/ndJ8cZIg4cM/maxresdefault.jpg')",
              }}
            >
              <span className="flex h-20 w-20 items-center justify-center rounded-full border border-white/[0.18] bg-black/[0.45] backdrop-blur transition-transform duration-300 group-hover:scale-105">
                <Play size={30} strokeWidth={2} className="ml-1 text-white" aria-hidden />
              </span>
            </div>
          </a>
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
