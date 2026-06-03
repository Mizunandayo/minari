"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

export function GlassCard({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className={
        "rounded-2xl border border-line bg-card p-6 " +
        "shadow-[0_1px_3px_rgba(67,41,24,0.06),0_12px_30px_-14px_rgba(67,41,24,0.18)] " +
        "transition-shadow duration-300 hover:shadow-[0_2px_6px_rgba(67,41,24,0.08),0_18px_40px_-16px_rgba(240,90,30,0.22)] " +
        className
      }
    >
      {children}
    </motion.div>
  );
}
