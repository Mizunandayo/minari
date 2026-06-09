"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Minus, X } from "lucide-react";



type Cell = "yes" | "partial" | "no";



const FEATURES = [
  "Detect flaky tests", "Diagnose root cause", "Generate fix", "Verify fix",
  "Create merge request", "Free", "Open source", "GitLab-native", "Multi-language",
] as const;




const COMPETITORS = [
  "Datadog", "Katalon", "Mergify", "BuildPulse", "Trunk", "TestDino", "Launchable", "Copilot",
] as const;





// rows = FEATURES, cols = COMPETITORS (Minari handled separately, always "yes").
const GRID: Cell[][] = [
  ["yes","yes","yes","yes","yes","yes","yes","partial"],   // detect
  ["partial","partial","no","no","no","no","no","partial"], // diagnose
  ["no","partial","no","no","no","no","no","partial"],      // generate fix
  ["no","no","no","no","no","no","no","no"],                // verify fix
  ["no","no","no","no","no","no","no","no"],                // create MR
  ["no","no","partial","partial","partial","yes","no","partial"], // free
  ["no","no","no","no","partial","no","no","no"],           // open source
  ["partial","partial","yes","partial","partial","no","partial","partial"], // gitlab-native
  ["yes","yes","partial","yes","yes","no","yes","yes"],     // multi-language
];

const ICON: Record<Cell, { node: React.ReactNode; label: string }> = {
  yes:     { node: <Check size={18} strokeWidth={2.6} style={{ color: "var(--color-pass)" }} />, label: "Yes" },
  partial: { node: <Minus size={18} strokeWidth={2.6} style={{ color: "var(--color-warn)" }} />, label: "Partial" },
  no:      { node: <X size={18} strokeWidth={2.6} style={{ color: "var(--color-crit)" }} />, label: "No" },
};

export function CompetitorMatrix() {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <div className="overflow-x-auto rounded-2xl border border-white/[0.14] bg-white/[0.035]">
      <table className="w-full min-w-[820px] border-collapse">
        <thead>
          <tr>
            <th className="sticky left-0 z-10 bg-[#0d0d0f] px-5 py-4 text-left text-[0.9375rem] font-semibold text-white">
              Capability
            </th>
            {COMPETITORS.map((c) => (
              <th key={c} className="px-3 py-4 text-center text-[0.875rem] font-semibold text-white/[0.78]">
                {c}
              </th>
            ))}
            <th className="px-3 py-4 text-center text-[0.9375rem] font-bold text-white">
              <span className="rounded-lg bg-[color:var(--color-pass)]/15 px-3 py-1.5"
                    style={{ color: "var(--color-pass)" }}>Minari</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {FEATURES.map((feature, r) => (
            <motion.tr
              key={feature}
              onMouseEnter={() => setHovered(r)}
              onMouseLeave={() => setHovered(null)}
              animate={{ backgroundColor: hovered === r ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0)" }}
              transition={{ duration: 0.18 }}
              className="border-t border-white/[0.06]"
            >
              <th scope="row"
                  className="sticky left-0 z-10 bg-[#0d0d0f] px-5 py-3.5 text-left text-[0.9375rem] font-medium text-white/[0.92]">
                {feature}
              </th>
              {GRID[r].map((cell, c) => (
                <td key={c} className="px-3 py-3.5 text-center" title={ICON[cell].label}>
                  <span className="inline-grid place-items-center" aria-label={ICON[cell].label}>
                    {ICON[cell].node}
                  </span>
                </td>
              ))}
              <td className="bg-[color:var(--color-pass)]/[0.06] px-3 py-3.5 text-center" title="Yes">
                <span className="inline-grid place-items-center" aria-label="Yes">
                  <Check size={18} strokeWidth={2.8} style={{ color: "var(--color-pass)" }} />
                </span>
              </td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
