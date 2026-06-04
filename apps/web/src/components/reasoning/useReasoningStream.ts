"use client";




import { useCallback, useRef, useState } from "react";
import type { ReasoningEvent } from "@/lib/types";










export function useReasoningStream() {
    const [events, setEvents] = useState<ReasoningEvent[]>([]);
    const [running, setRunning] = useState(false);
    const abortRef = useRef<AbortController | null>(null);





  const start = useCallback(async (url: string) => {
    abortRef.current?.abort();
    const ac = new AbortController();
    abortRef.current = ac;
    setEvents([]);
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
        // sse-starlette uses CRLF (\r\n) line endings; normalize to \n so the
        // frame split on "\n\n" and the per-line "data:" lookup both work.
        buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
        const frames = buffer.split("\n\n");
        buffer = frames.pop() ?? "";
        for (const frame of frames) {
          const dataLine = frame.split("\n").find((l) => l.startsWith("data:"));
          if (!dataLine) continue;
          try {
            const evt = JSON.parse(dataLine.slice(5).trim()) as ReasoningEvent;
            setEvents((prev) => [...prev, evt]);
            if (evt.type === "done" || evt.type === "error") setRunning(false);
          } catch { /* ignore keep-alive pings */ }
        }
      }
    } finally {
      setRunning(false);
    }
  }, []);






  const stop = useCallback(() => abortRef.current?.abort(), []);
  return { events, running, start, stop };
}
