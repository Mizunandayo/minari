import { MetricGrid } from "@/components/ui/MetricGrid";
import { Button } from "@/components/ui/Button";
import { Activity } from "lucide-react";

export default function Home() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <header className="mb-12">
        <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-line bg-primary/5 px-4 py-1.5 text-[0.875rem] font-semibold text-ink-muted">
          <Activity size={16} strokeWidth={2.4} className="text-primary" aria-hidden />
          GitLab Track · Rapid Agent Hackathon 2026
        </div>
        <h1 className="text-5xl font-bold leading-tight tracking-tight text-ink">
          Minari<span className="ml-3 align-middle text-2xl font-semibold text-clay">実成</span>
        </h1>
        <p className="mt-4 max-w-2xl text-lg font-normal text-ink-soft">
          Autonomous flaky-test intelligence. Detect, diagnose, fix, verify, and deliver —
          end to end through GitLab MCP, in under two minutes.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Button aria-label="View live diagnosis">Watch a live diagnosis</Button>
          <Button variant="ghost" aria-label="Open competitor comparison">Compare vs. Datadog</Button>
        </div>
      </header>
      <MetricGrid />
    </main>
  );
}
