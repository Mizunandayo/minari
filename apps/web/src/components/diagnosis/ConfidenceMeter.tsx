"use client";


import { motion } from "framer-motion";










export function ConfidenceMeter({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const tone = value >= 0.7 ? "var(--color-pass)" : value >= 0.4 ? "var(--color-warn)" : "var(--color-crit)";
  return (
    <div>
      <div className="flex items-baseline justify-between">
        <span className="text-[0.875rem] font-medium text-white/[0.78]">Confidence</span>
        <span className="text-2xl font-bold" style={{ color: tone }}>{pct}%</span>
      </div>
      <div className="mt-2 h-2.5 w-full overflow-hidden rounded-full bg-white/[0.10]">
        <motion.div
          initial={{ width: 0 }} animate={{ width: `${pct}%` }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="h-full rounded-full" style={{ background: tone }}
        />
      </div>
    </div>
  );
}
