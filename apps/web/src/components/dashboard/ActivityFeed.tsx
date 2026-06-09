import { ExternalLink } from "lucide-react";
import { CategoryTag } from "@/components/diagnosis/CategoryTag";
import { getDashboardActivity } from "@/lib/api";
import type { ActivityItem } from "@/lib/types";





function ago(iso: string) {
  const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return `${Math.round(s)}s ago`;
  if (s < 3600) return `${Math.round(s / 60)}m ago`;
  if (s < 86400) return `${Math.round(s / 3600)}h ago`;
  return `${Math.round(s / 86400)}d ago`;
}




export async function ActivityFeed() {
  let items: ActivityItem[] = [];
  try { items = await getDashboardActivity(); } catch { items = []; }

  if (items.length === 0) {
    return (
      <p className="rounded-2xl border border-white/[0.14] bg-white/[0.035] px-6 py-8 text-[0.9375rem] font-medium text-white/[0.92]">
        No merge requests delivered yet. Run a diagnosis to populate the feed.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-2xl border border-white/[0.14] bg-white/[0.035]">
      <table className="w-full min-w-[640px] border-collapse">
        <thead>
          <tr className="border-b border-white/[0.10] text-left">
            {["Test", "Root cause", "Confidence", "When", "Merge request"].map((h) => (
              <th key={h} className="px-5 py-3.5 text-[0.875rem] font-semibold text-white/[0.78]">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((it, i) => (
            <tr key={`${it.test_name}-${i}`}
                className="border-b border-white/[0.06] transition-colors last:border-0 hover:bg-white/[0.04]">
              <td className="px-5 py-4">
                <p className="font-mono text-[0.9375rem] text-white">{it.test_name}</p>
                <p className="font-mono text-[0.8125rem] text-white/[0.78]">{it.file_path}</p>
              </td>
              <td className="px-5 py-4">
                {it.category ? <CategoryTag category={it.category} />
                  : <span className="text-[0.9375rem] text-white/[0.78]">—</span>}
              </td>
              <td className="px-5 py-4 text-[0.9375rem] font-semibold text-white">
                {it.confidence !== null ? `${Math.round(it.confidence * 100)}%` : "—"}
              </td>
              <td className="px-5 py-4 text-[0.9375rem] font-medium text-white/[0.92]">
                {ago(it.created_at)}
              </td>
              <td className="px-5 py-4">
                {it.mr_url ? (
                  <a href={it.mr_url} target="_blank" rel="noopener noreferrer"
                     className="inline-flex cursor-pointer items-center gap-1.5 text-[0.9375rem] font-semibold text-[color:var(--color-info)] transition-opacity hover:opacity-80 focus-visible:outline-none"
                     aria-label={`Open merge request ${it.mr_iid ?? ""} in GitLab`}>
                    !{it.mr_iid} <ExternalLink size={15} strokeWidth={2.4} aria-hidden />
                  </a>
                ) : <span className="text-[0.9375rem] text-white/[0.78]">—</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
