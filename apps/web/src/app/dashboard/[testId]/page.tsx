import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { DEMO_PROJECT_ID, getTests } from "@/lib/api";
import { DiagnosisCard } from "@/components/diagnosis/DiagnosisCard";
import { ReasoningPanel } from "@/components/reasoning/ReasoningPanel";

// Next 16: dynamic route params are async — must be awaited.
export default async function TestDetailPage({
  params,
}: {
  params: Promise<{ testId: string }>;
}) {
  const { testId } = await params;

  const tests = await getTests().catch(() => []);
  const test = tests.find((t) => t.id === testId);

  if (!test) {
    return (
      <main className="mx-auto max-w-5xl px-6 py-12">
        <Link
          href="/dashboard"
          className="mb-8 inline-flex items-center gap-2 text-[0.9375rem] font-semibold text-white/[0.78] transition-colors hover:text-white"
        >
          <ArrowLeft size={18} strokeWidth={2.2} aria-hidden />
          Back to tests
        </Link>
        <p className="text-lg font-semibold text-white">Test not found.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <Link
        href="/dashboard"
        className="mb-8 inline-flex items-center gap-2 text-[0.9375rem] font-semibold text-white/[0.78] transition-colors hover:text-white"
      >
        <ArrowLeft size={18} strokeWidth={2.2} aria-hidden />
        Back to tests
      </Link>

      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-white">{test.test_name}</h1>
        <p className="mt-2 text-[0.9375rem] font-medium text-white/[0.78]">{test.file_path}</p>
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[320px_1fr]">
        <DiagnosisCard category={test.category} confidence={test.confidence} />
        <ReasoningPanel
          projectId={DEMO_PROJECT_ID}
          filePath={test.file_path}
          testName={test.test_name}
        />
      </div>
    </main>
  );
}
