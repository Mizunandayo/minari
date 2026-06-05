"use client";

import { Highlight, themes } from "prism-react-renderer";


const PRISM_LANG: Record<string, string> = {
  python: "python", javascript: "jsx", typescript: "tsx", go: "go", java: "java",
};



type Line = { text: string; kind: "add" | "del" | "ctx" | "meta" };


function parse(diff: string): Line[] {
  return diff.split("\n").map((raw) => {
    if (raw.startsWith("+++") || raw.startsWith("---") || raw.startsWith("@@") || raw.startsWith("diff"))
      return { text: raw, kind: "meta" as const };
    if (raw.startsWith("+")) return { text: raw.slice(1), kind: "add" as const };
    if (raw.startsWith("-")) return { text: raw.slice(1), kind: "del" as const };
    return { text: raw.replace(/^ /, ""), kind: "ctx" as const };
  });
}


const BG: Record<Line["kind"], string> = {
  add: "color-mix(in srgb, var(--color-pass) 14%, transparent)",
  del: "color-mix(in srgb, var(--color-crit) 14%, transparent)",
  ctx: "transparent",
  meta: "rgba(255,255,255,0.04)",
};
const SIGN: Record<Line["kind"], string> = { add: "+", del: "−", ctx: " ", meta: " " };
const SIGN_COLOR: Record<Line["kind"], string> = {
  add: "var(--color-pass)", del: "var(--color-crit)",
  ctx: "var(--color-text-meta)", meta: "var(--color-text-meta)",
};




export function DiffView({ diff, language }: { diff: string; language: string }) {
  const lines = parse(diff);
  const lang = PRISM_LANG[language] ?? "python";



  return (
    <div className="overflow-x-auto rounded-xl border border-white/[0.12] bg-[#08080a]">
      <pre className="m-0 p-0 font-mono text-[0.875rem] leading-relaxed">
        {lines.map((line, i) => (
          <div key={i} className="flex" style={{ background: BG[line.kind] }}>
            <span
              className="select-none px-3 py-0.5 text-right"
              style={{ color: SIGN_COLOR[line.kind], minWidth: "2rem" }}
              aria-hidden
            >
              {SIGN[line.kind]}
            </span>
            <Highlight code={line.text} language={lang} theme={themes.vsDark}>
              {({ tokens, getTokenProps }) => (
                <code className="flex-1 py-0.5 pr-4 text-white/[0.92]">
                  {tokens[0]?.map((token, k) => <span key={k} {...getTokenProps({ token })} />)}
                </code>
              )}
            </Highlight>
          </div>
        ))}
      </pre>
    </div>
  );
}