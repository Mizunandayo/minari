"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "ghost";
  type?: "button" | "submit";
  "aria-label"?: string;
};

export function Button({ children, onClick, variant = "primary", type = "button", ...rest }: Props) {
  const base =
    "inline-flex items-center gap-2 rounded-xl px-5 py-3 text-base font-semibold " +
    "cursor-pointer select-none transition-[transform,background,border-color,color] duration-200 " +
    "ease-out focus-visible:outline-none";
  const styles =
    variant === "primary"
      ? "bg-primary text-white shadow-[0_6px_18px_-6px_rgba(240,90,30,0.5)] hover:bg-primary-strong"
      : "border border-line text-ink hover:border-primary hover:text-primary hover:bg-primary/5";

  return (
    <motion.button
      type={type}
      onClick={onClick}
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.97 }}
      className={`${base} ${styles}`}
      {...rest}
    >
      {children}
    </motion.button>
  );
}
