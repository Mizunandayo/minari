"""Persist validated fix candidates"""

from __future__ import annotations

from app.db.session import get_pool
from app.schemas.fix import FixCandidate


async def create_fixes(diagnosis_id: str, candidates: list[FixCandidate]) -> int:
    """Insert safe candidates (re-ranked 1..n). Returns rows written."""
    pool = get_pool()
    if pool is None or not candidates:
        return 0
    written = 0
    async with pool.acquire() as conn:
        for new_rank, c in enumerate(candidates, start=1):
            await conn.execute(
                """
                insert into fixes
                  (diagnosis_id, rank, fix_diff, confidence, fix_category,
                   explanation, assertions_modified)
                values ($1, $2, $3, $4, $5, $6, false)
                """,
                diagnosis_id, new_rank, c.fix_diff, c.confidence,
                c.fix_category.value, c.explanation,
            )
            written += 1
    return written
