"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence } from "framer-motion";
import { Play, Pause } from "lucide-react";
import { useReasoningStream } from "./useReasoningStream";
import { EventCard } from "./EventCard";
import { startDiagnosis, streamUrl } from "@/lib/api";
import { Button } from "@/components/ui/Button";





export function ReasoningPanel({ projectId, filePath, testName }: {
  projectId: string; filePath: string; testName: string;
}) {
  const { events, running, start, stop } = useReasoningStream();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [events]);

  async function run() {
    const accepted = await startDiagnosis({ project_id: projectId, file_path: filePath, test_name: testName });
    await start(streamUrl(accepted.stream_path, accepted.stream_token));
  }





  return (
    <section className="rounded-2xl border border-white/[0.14] bg-[#08080a] shadow-[0_8px_40px_-12px_rgba(0,0,0,0.7)]">
      <header className="flex items-center justify-between border-b border-white/[0.10] px-5 py-3.5">
        <div className="flex items-center gap-2.5">
          <span className="h-2.5 w-2.5 rounded-full" style={{ background: running ? "var(--color-pass)" : "var(--color-text-meta)" }} />
          <h2 className="text-base font-semibold text-white">Live Agent Reasoning</h2>
        </div>
        <Button variant="ghost" onClick={running ? stop : run} aria-label={running ? "Pause stream" : "Run diagnosis"}>
          {running ? <Pause size={16} strokeWidth={2.2} /> : <Play size={16} strokeWidth={2.2} />}
          {running ? "Pause" : "Run diagnosis"}
        </Button>
      </header>
      <div ref={scrollRef} className="max-h-[28rem] overflow-y-auto px-5 py-3">
        {events.length === 0 && (
          <p className="py-10 text-center text-[0.9375rem] text-white/[0.78]">
            Press “Run diagnosis” to watch Minari reason through this test in real time.
          </p>
        )}
        <AnimatePresence initial={false}>
          {events.map((e, i) => <EventCard key={`${e.ts_ms}-${i}`} event={e} />)}
        </AnimatePresence>
      </div>
    </section>
  );
}
