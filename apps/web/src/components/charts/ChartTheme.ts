// Single source of truth so every chart obeys the Mi design tokens


export const CHART = {
  axisTick: { fill: "rgba(255,255,255,0.78)", fontSize: 13, fontFamily: "inherit" },
  grid: "rgba(255,255,255,0.08)",
  info: "#60a5fa",  
  pass: "#34d399",   
  warn: "#fbbf24",    
  crit: "#f87171",    
  text: "rgba(255,255,255,0.92)",
  meta: "rgba(255,255,255,0.78)",
} as const;

// Donut opacity ramp (descending, ranked by slice count). One hue, on-system.
export const RAMP = [1.0, 0.78, 0.58, 0.4, 0.26] as const;