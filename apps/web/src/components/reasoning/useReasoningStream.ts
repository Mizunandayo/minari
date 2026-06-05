"use client";

import { useCallback, useRef, useState } from "react";
import type { ReasoningEvent, FixStreamEvent, AnyStreamEvent, FixCandidate } from "@/lib/types";

export function useReasoningStream() {
  const [events, setEvents] = useState<ReasoningEvent[]>([]);
  const [fixes, setFixes] = useState<FixCandidate[]>([]);
  const [running, setRunning] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  
  const start = useCallback(async (url: string) => {
    abortRef.current?.abort();
    const ac = new AbortController();
    abortRef.current = ac;
    setEvents([]);
    setFixes([]);
    setRunning(true);



    const res = await fetch(url, { signal: ac.signal });
    if (!res.body) { setRunning(false); return; }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    try {
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
        const frames = buffer.split("\n\n");
        buffer = frames.pop() ?? "";
        for (const frame of frames) {
          const dataLine = frame.split("\n").find((l) => l.startsWith("data:"));
          if (!dataLine) continue;
          try {
            const evt = JSON.parse(dataLine.slice(5).trim()) as AnyStreamEvent;
            if (evt.type === "fix") {
              const f = evt as FixStreamEvent;
              setFixes((prev) => [...prev, {
                rank: f.rank, fix_category: f.fix_category, confidence: f.confidence,
                explanation: f.explanation, fix_diff: f.fix_diff, language: f.language,
              }]);
            } else {
              setEvents((prev) => [...prev, evt as ReasoningEvent]);
              if (evt.type === "done" || evt.type === "error") setRunning(false);
            }
          } catch { /* ignore keep-alive pings */ }
        }
      }
    } finally {
      setRunning(false);
    }
  }, []);

  const stop = useCallback(() => abortRef.current?.abort(), []);
  return { events, fixes, running, start, stop };
}
