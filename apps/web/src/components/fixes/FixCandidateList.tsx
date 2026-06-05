"use client";

import { Wrench } from "lucide-react";
import type { FixCandidate } from "@/lib/types";
import { FixCandidateCard } from "./FixCandidateCard";



export function FixCandidateList({ fixes }: { fixes: FixCandidate[] }) {
  if (fixes.length === 0) return null;
  const ranked = [...fixes].sort((a, b) => a.rank - b.rank);
  

  return (
    <section className="mt-8">
      <header className="mb-4 flex items-center gap-2.5">
        <Wrench size={20} strokeWidth={2.2} className="text-white" aria-hidden />
        <h2 className="text-xl font-bold text-white">
          Fix candidates <span className="text-white/[0.78]">({ranked.length})</span>
        </h2>
      </header>
      <div className="flex flex-col gap-4">
        {ranked.map((fix, i) => (
          <FixCandidateCard key={fix.rank} fix={fix} defaultOpen={i === 0} />
        ))}
      </div>
    </section>
  );
}