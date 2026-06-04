import Link from "next/link";
import { MetricGrid } from "@/components/ui/MetricGrid";
import { Button } from "@/components/ui/Button";
import { Activity, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <header className="mb-12">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/15 px-4 py-1.5 text-[0.875rem] font-medium text-white/[0.78]">
          <Activity size={16} strokeWidth={2.2} aria-hidden />
          GitLab Track · Rapid Agent Hackathon 2026
        </div>
        <h1 className="text-5xl font-bold leading-tight tracking-tight text-white">
          Minari<span className="ml-3 align-middle text-2xl font-medium text-white/[0.78]">実成</span>
        </h1>
        <p className="mt-4 max-w-2xl text-lg font-normal text-white/[0.92]">
          Autonomous flaky-test intelligence. Detect, diagnose, fix, verify, and deliver —
          end to end through GitLab MCP, in under two minutes.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link
            href="/dashboard"
            aria-label="Open the live diagnosis dashboard"
            className="inline-flex cursor-pointer items-center gap-2 rounded-xl bg-white px-5 py-3 text-base font-semibold text-black transition-[transform,background] duration-200 ease-out hover:-translate-y-0.5 hover:bg-white/90 focus-visible:outline-none"
          >
            Watch a live diagnosis
            <ArrowRight size={18} strokeWidth={2.4} aria-hidden />
          </Link>
          <Button variant="ghost" aria-label="Open competitor comparison">Compare vs. Datadog</Button>
        </div>
      </header>
      <MetricGrid />
    </main>
  );
}
