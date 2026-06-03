import { MetricCard } from "@/components/ui/MetricCard";

// Day 1: static seed data. Day 2 swaps in the live API client (lib/api.ts).
export function MetricGrid() {
  return (
    <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard label="Tests Fixed" value="6" trend="+6 this week" severity="pass" />
      <MetricCard label="Average Fix Time" value="94s" trend="failure to merge request" />
      <MetricCard label="Success Rate" value="92%" trend="11 of 12 verified" severity="pass" />
      <MetricCard label="Flakiness Rate" value="8.4%" trend="trending down" severity="warn" />
    </section>
  );
}
