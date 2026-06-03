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
    "cursor-pointer select-none transition-[transform,background,border-color] duration-200 " +
    "ease-out focus-visible:outline-none";
  const styles =
    variant === "primary"
      ? "bg-white text-black hover:bg-white/90"
      : "border border-white/20 text-white hover:border-white/45 hover:bg-white/5";

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
