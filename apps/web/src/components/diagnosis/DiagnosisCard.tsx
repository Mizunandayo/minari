import type { RootCause } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { CategoryTag } from "./CategoryTag";
import { ConfidenceMeter } from "./ConfidenceMeter";

type Props = {
  category: RootCause | null;
  confidence: number | null;
};

// The last persisted diagnosis summary for a test. Live detail (reasoning chain)
// streams in the ReasoningPanel; this is the at-a-glance verdict.
export function DiagnosisCard({ category, confidence }: Props) {
  return (
    <GlassCard>
      <p className="text-[0.875rem] font-semibold uppercase tracking-wide text-white/[0.78]">
        Latest diagnosis
      </p>
      {category ? (
        <div className="mt-4 flex flex-col gap-5">
          <CategoryTag category={category} />
          {confidence !== null && <ConfidenceMeter value={confidence} />}
        </div>
      ) : (
        <p className="mt-4 text-[0.9375rem] font-medium text-white/[0.92]">
          Not yet diagnosed. Run a diagnosis to generate a root-cause verdict.
        </p>
      )}
    </GlassCard>
  );
}
