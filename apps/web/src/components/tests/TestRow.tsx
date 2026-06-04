"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ChevronRight } from "lucide-react";
import type { TestListItem } from "@/lib/types";
import { PfsBadge } from "./PfsBadge";
import { CategoryTag } from "@/components/diagnosis/CategoryTag";

export function TestRow({ test }: { test: TestListItem }) {
  return (
    <Link href={`/dashboard/${test.id}`} aria-label={`Open diagnosis for ${test.test_name}`}>
      <motion.div
        whileHover={{ y: -2 }}
        transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
        className="flex cursor-pointer items-center justify-between gap-4 rounded-2xl border border-white/[0.14] bg-white/[0.035] px-5 py-4 backdrop-blur-xl transition-colors hover:border-white/30"
      >
        <div className="min-w-0">
          <p className="truncate text-lg font-semibold text-white">{test.test_name}</p>
          <p className="mt-1 truncate text-[0.875rem] font-medium text-white/[0.78]">
            {test.file_path}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-3">
          {test.category && <CategoryTag category={test.category} />}
          <PfsBadge score={test.pfs_score} />
          <ChevronRight size={20} strokeWidth={2.2} className="text-white/[0.78]" aria-hidden />
        </div>
      </motion.div>
    </Link>
  );
}
