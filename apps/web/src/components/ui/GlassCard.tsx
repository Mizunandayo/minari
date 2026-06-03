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
        "rounded-2xl border border-white/[0.14] bg-white/[0.035] p-6 " +
        "backdrop-blur-xl shadow-[0_8px_40px_-12px_rgba(0,0,0,0.6)] " +
        className
      }
    >
      {children}
    </motion.div>
  );
}
