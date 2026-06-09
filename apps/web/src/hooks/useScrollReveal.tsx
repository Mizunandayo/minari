"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";

/**
 * Reveal — fades + lifts its children into view once, the first time they
 * cross the viewport. Respects prefers-reduced-motion (globals.css disables the
 * transition, so the element simply appears). Ported from the Mirai deck.
 */
export function Reveal({
  children,
  delay = 0,
  as: Tag = "div",
  className = "",
}: {
  children: ReactNode;
  delay?: 0 | 1 | 2 | 3 | 4 | 5;
  as?: "div" | "section" | "li" | "article";
  className?: string;
}) {
  const ref = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const obs = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            setVisible(true);
            obs.disconnect();
          }
        }
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" },
    );
    obs.observe(node);
    return () => obs.disconnect();
  }, []);

  const delayClass = delay ? `reveal-d${delay}` : "";
  return (
    <Tag
      ref={ref as never}
      className={`reveal ${delayClass} ${visible ? "visible" : ""} ${className}`.trim()}
    >
      {children}
    </Tag>
  );
}
