"use client";

import { motion } from "framer-motion";
import type { ReasoningEvent } from "@/lib/types";

function pct(x: number) {
  return `${Math.round(x * 100)}%`;
}




export function ConfidenceCascade({ events }: { events: ReasoningEvent[] }) {
  const merge = [...events].reverse().find((e) => e.type === "merge");
  if (!merge || merge.type !== "merge") return null;

  const steps = [
    { label: "Detection", value: merge.detection_confidence },
    { label: "Diagnosis", value: merge.diagnosis_confidence },
    { label: "Fix", value: merge.fix_confidence },
    { label: "Verification", value: merge.verification_confidence },
  ];
  const overall = merge.overall_confidence;
  const tone =
    overall >= 0.7 ? "var(--color-pass)" : overall >= 0.4 ? "var(--color-warn)" : "var(--color-crit)";





  return (
    <section className="mt-6 rounded-2xl border border-white/[0.14] bg-[#0d0d0f] p-5">
      <h3 className="mb-4 text-base font-semibold text-white">Confidence Cascade</h3>
      <div className="space-y-3">
        {steps.map((s, i) => (
          <div key={s.label} className="flex items-center gap-3">
            <span className="w-28 text-[0.9375rem] font-medium text-white/[0.92]">{s.label}</span>
            <div className="relative h-3 flex-1 overflow-hidden rounded-full bg-white/[0.10]">
              <motion.div
                className="absolute inset-y-0 left-0 rounded-full"
                style={{ background: "var(--color-info)" }}
                initial={{ width: 0 }}
                animate={{ width: pct(s.value) }}
                transition={{ duration: 0.5, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
            <span className="w-14 text-right text-[0.9375rem] font-semibold text-white">
              {pct(s.value)}
            </span>
          </div>
        ))}
      </div>
      <div className="mt-5 flex items-center justify-between border-t border-white/[0.10] pt-4">
        <span className="text-[0.9375rem] font-semibold text-white/[0.92]">Overall confidence</span>
        <motion.span
          className="text-2xl font-bold"
          style={{ color: tone }}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.45, duration: 0.4 }}
        >
          {pct(overall)}
        </motion.span>
      </div>
    </section>
  );
}
