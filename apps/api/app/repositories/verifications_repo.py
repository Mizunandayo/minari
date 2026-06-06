"""Persist verification results to the existing verifications table"""



from __future__ import annotations

import json

from app.db.session import get_pool
from app.schemas.verification import VerificationReport


async def create_verification(fix_id: str, report: VerificationReport) -> str | None:
    pool = get_pool()
    if pool is None:
        return None
    run_results = json.dumps([r.model_dump() for r in report.run_results])
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            insert into verifications
              (fix_id, branch_name, pipeline_id, run_results, pass_rate,
               variance_before, variance_after, variance_reduction_pct,
               gate_passed, healing_attempts)
            values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
            returning id
            """,
            fix_id, report.branch_name, report.pipeline_id, run_results,
            report.pass_rate, report.variance_before, report.variance_after,
            report.variance_reduction_pct, report.gate_passed,
            min(report.healing_attempts, 2),     
        )
    return str(row["id"]) if row else None

