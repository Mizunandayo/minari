"use client";

import { motion } from "framer-motion";
import { GitPullRequest, ExternalLink, UserCheck } from "lucide-react";
import type { ReasoningEvent } from "@/lib/types";





export function MergeRequestCard({ events }: { events: ReasoningEvent[] }) {
  const merge = [...events].reverse().find((e) => e.type === "merge");
  if (!merge || merge.type !== "merge" || merge.mr_iid === null) return null;




  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="mt-6 rounded-2xl border-2 p-5"
      style={{ borderColor: "var(--color-pass)", background: "rgba(52,211,153,0.06)" }}
    >
      <div className="flex items-center gap-3">
        <GitPullRequest size={24} strokeWidth={2.2} style={{ color: "var(--color-pass)" }} aria-hidden />
        <h3 className="text-lg font-bold text-white">Merge request opened</h3>
      </div>
      <p className="mt-2 text-[0.9375rem] font-medium text-white/[0.92]">
        Minari opened <span className="font-semibold text-white">!{merge.mr_iid}</span> with the
        verified fix, the full diagnosis, and the 5-run verification report attached.
      </p>
      {merge.assigned_to && (
        <p className="mt-2 inline-flex items-center gap-2 text-[0.9375rem] font-medium text-white/[0.92]">
          <UserCheck size={18} strokeWidth={2.2} style={{ color: "var(--color-pass)" }} aria-hidden />
          Reviewer: <span className="font-semibold text-white">{merge.assigned_to}</span>
        </p>
      )}
      {merge.mr_url && (
        <a
          href={merge.mr_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-flex items-center gap-2 rounded-xl px-5 py-2.5 text-[0.9375rem] font-semibold text-black transition-transform duration-200 hover:-translate-y-0.5"
          style={{ background: "var(--color-pass)" }}
        >
          Review in GitLab
          <ExternalLink size={18} strokeWidth={2.4} aria-hidden />
        </a>
      )}
    </motion.section>
  );
}
