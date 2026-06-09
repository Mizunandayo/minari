import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import {
  getDashboardRootCauses, getDashboardTrends, getTests,
} from "@/lib/api";
import { GlassCard } from "@/components/ui/GlassCard";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { MetricGridLive } from "@/components/dashboard/MetricGridLive";
import { ActivityFeed } from "@/components/dashboard/ActivityFeed";
import { CompetitorMatrix } from "@/components/dashboard/CompetitorMatrix";
import { FlakinessTrend } from "@/components/charts/FlakinessTrend";
import { RootCauseDonut } from "@/components/charts/RootCauseDonut";
import { TestList } from "@/components/tests/TestList";
import type { RootCauseSlice, TestListItem, TrendPoint } from "@/lib/types";






export default async function DashboardPage() {
  let tests: TestListItem[] = [];
  let trends: TrendPoint[] = [];
  let rootCauses: RootCauseSlice[] = [];
  let error: string | null = null;
  try {
    [tests, trends, rootCauses] = await Promise.all([
      getTests(), getDashboardTrends(), getDashboardRootCauses(),
    ]);
  } catch {
    error = "Could not reach the Minari API. Is the backend running on :8000?";
  }

  return (
    <main className="mx-auto max-w-6xl px-5 py-10 sm:px-6 sm:py-12">
      <Link href="/"
        className="mb-8 inline-flex items-center gap-2 text-[0.9375rem] font-semibold text-white/[0.78] transition-colors hover:text-white">
        <ArrowLeft size={18} strokeWidth={2.2} aria-hidden />
        Back to overview
      </Link>

      <header className="mb-10">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">Dashboard</h1>
        <p className="mt-3 max-w-2xl text-lg font-normal text-white/[0.92]">
          Live flakiness intelligence across the demo project — detection through delivery.
        </p>
      </header>

      {error && (
        <div className="mb-10 rounded-2xl border border-[color:var(--color-crit)]/40 bg-white/[0.035] px-6 py-8">
          <p className="text-lg font-semibold text-[color:var(--color-crit)]">{error}</p>
        </div>
      )}

      <div className="mb-12">
        <MetricGridLive />
      </div>

      <div className="mb-12 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <GlassCard>
          <SectionHeading title="Flakiness Trend" hint="Daily flaky-run rate, last 30 days" />
          <FlakinessTrend data={trends} />
        </GlassCard>
        <GlassCard>
          <SectionHeading title="Root Cause Distribution" hint="Latest diagnosis per test" />
          <RootCauseDonut data={rootCauses} />
        </GlassCard>
      </div>

      <section className="mb-12">
        <SectionHeading title="Recent Activity" hint="The last ten delivered merge requests" />
        <ActivityFeed />
      </section>

      <section className="mb-12">
        <SectionHeading title="How Minari Compares"
          hint="Every competitor stops at detection. Minari completes all five stages." />
        <CompetitorMatrix />
      </section>

      <section>
        <SectionHeading title="Tracked Tests" hint="Open one to watch a live diagnosis stream." />
        <TestList tests={tests} />
      </section>
    </main>
  );
}
