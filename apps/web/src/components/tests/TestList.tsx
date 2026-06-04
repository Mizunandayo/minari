import type { TestListItem } from "@/lib/types";
import { TestRow } from "./TestRow";

export function TestList({ tests }: { tests: TestListItem[] }) {
  if (tests.length === 0) {
    return (
      <div className="rounded-2xl border border-white/[0.14] bg-white/[0.035] px-6 py-12 text-center">
        <p className="text-lg font-semibold text-white">No tests tracked yet</p>
        <p className="mt-2 text-[0.9375rem] font-medium text-white/[0.78]">
          Run a diagnosis from a test detail page and it will appear here.
        </p>
      </div>
    );
  }
  return (
    <div className="flex flex-col gap-3">
      {tests.map((t) => (
        <TestRow key={t.id} test={t} />
      ))}
    </div>
  );
}
