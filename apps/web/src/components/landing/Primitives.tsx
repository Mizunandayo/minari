import type { ReactNode } from "react";
import { ImageIcon } from "lucide-react";

/** Uppercase eyebrow label that opens every landing section. */
export function MicroLabel({ children, center = false }: { children: ReactNode; center?: boolean }) {
  return (
    <p
      className={`mb-5 text-[0.78rem] font-bold uppercase tracking-[0.14em] text-white/[0.78] ${
        center ? "text-center" : ""
      }`}
    >
      {children}
    </p>
  );
}

/** Section heading with an optional muted second line (the Mirai two-tone H2). */
export function DisplayHeading({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <h2
      className={`font-bold leading-[1.04] tracking-[-0.04em] text-white ${className}`}
      style={{ fontSize: "clamp(2.2rem,5vw,3.8rem)" }}
    >
      {children}
    </h2>
  );
}

/**
 * Captioned glass frame standing in for a product screenshot. Drop a real PNG
 * into /public/screenshots and pass `src` to swap the placeholder for the image.
 */
export function PlaceholderFrame({
  caption,
  src,
  ratio = "16 / 9",
}: {
  caption: string;
  src?: string;
  ratio?: string;
}) {
  return (
    <figure className="overflow-hidden rounded-2xl border border-white/[0.14] bg-white/[0.03]">
      {src ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={src} alt={caption} className="block h-auto w-full" />
      ) : (
        <div
          className="flex w-full flex-col items-center justify-center gap-3"
          style={{
            aspectRatio: ratio,
            background:
              "repeating-linear-gradient(135deg, rgba(255,255,255,0.02) 0 14px, transparent 14px 28px)",
          }}
        >
          <span className="flex h-12 w-12 items-center justify-center rounded-xl border border-white/[0.18] bg-white/[0.03]">
            <ImageIcon size={22} strokeWidth={1.8} className="text-white/[0.78]" aria-hidden />
          </span>
          <figcaption className="px-6 text-center text-[0.9rem] font-semibold text-white/[0.78]">
            {caption}
          </figcaption>
        </div>
      )}
    </figure>
  );
}
