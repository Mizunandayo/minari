"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, ChevronDown, ChevronRight } from "lucide-react";
import type { FixCandidate } from "@/lib/types";
import { ConfidenceMeter } from "@/components/diagnosis/ConfidenceMeter";
import { DiffView } from "./DiffView";




const CATEGORY_LABEL: Record<FixCandidate["fix_category"], string> = {
  sync: "Synchronization", wait: "Explicit Wait", isolate: "Isolation",
  timeout: "Timeout Tuning", resource: "Resource Limit",
};





export function FixCandidateCard({ fix, defaultOpen = false }: { fix: FixCandidate; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <motion.article
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className="rounded-2xl border border-white/[0.14] bg-[var(--color-surface-raised)] p-5"
    >
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full cursor-pointer items-center justify-between gap-4 text-left"
        aria-expanded={open}
      >
        <div className="flex items-center gap-3">
          <span className="grid h-8 w-8 place-items-center rounded-lg border border-white/20 text-base font-bold text-white">
            {fix.rank}
          </span>
          <div>
            <p className="text-lg font-semibold text-white">{CATEGORY_LABEL[fix.fix_category]}</p>
            <span className="inline-flex items-center gap-1.5 text-[0.875rem] font-semibold text-[var(--color-pass)]">
              <ShieldCheck size={16} strokeWidth={2.2} aria-hidden />
              Assertions preserved
            </span>
          </div>
        </div>
        {open ? <ChevronDown size={20} aria-hidden /> : <ChevronRight size={20} aria-hidden />}
      </button>

      <div className="mt-4">
        <ConfidenceMeter value={fix.confidence} />
      </div>
      <p className="mt-4 text-base font-medium text-white/[0.92]">{fix.explanation}</p>

      <motion.div
        initial={false}
        animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
        className="overflow-hidden"
      >
        <div className="mt-4">
          <DiffView diff={fix.fix_diff} language={fix.language} />
        </div>
      </motion.div>
    </motion.article>
  );
}
