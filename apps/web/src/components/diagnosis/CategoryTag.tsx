import type { RootCause } from "@/lib/types";




const LABEL: Record<RootCause, string> = {
  async: "Async / Timing", race: "Race Condition", resource: "Resource Contention",
  network: "Network Dependency", data: "Data Isolation",
};






export function CategoryTag({ category }: { category: RootCause }) {
  return (
    <span className="inline-flex items-center rounded-full border border-white/20 px-3.5 py-1 text-[0.875rem] font-semibold text-white">
      {LABEL[category]}
    </span>
  );
}