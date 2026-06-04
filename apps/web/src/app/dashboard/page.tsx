import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { getTests } from "@/lib/api";
import { TestList } from "@/components/tests/TestList";
import type { TestListItem } from "@/lib/types";

// Server component: fetches the tracked tests on the server (no client bundle cost).
export default async function DashboardPage() {
  let tests: TestListItem[] = [];
  let error: string | null = null;
  try {
    tests = await getTests();
  } catch {
    error = "Could not reach the Minari API. Is the backend running on :8000?";
  }

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <Link
        href="/"
        className="mb-8 inline-flex items-center gap-2 text-[0.9375rem] font-semibold text-white/[0.78] transition-colors hover:text-white"
      >
        <ArrowLeft size={18} strokeWidth={2.2} aria-hidden />
        Back to overview
      </Link>

      <header className="mb-10">
        <h1 className="text-4xl font-bold tracking-tight text-white">Tracked tests</h1>
        <p className="mt-3 max-w-2xl text-lg font-normal text-white/[0.92]">
          Every test Minari has analyzed, with its latest root-cause verdict. Open one to
          watch a live diagnosis stream end to end.
        </p>
      </header>

      {error ? (
        <div className="rounded-2xl border border-[color:var(--color-crit)]/40 bg-white/[0.035] px-6 py-8">
          <p className="text-lg font-semibold text-[color:var(--color-crit)]">{error}</p>
        </div>
      ) : (
        <TestList tests={tests} />
      )}
    </main>
  );
}
