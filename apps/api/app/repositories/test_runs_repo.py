"""Test-run history real pfs"""

from __future__ import annotations

from app.db.session import get_pool
from app.services.pfs.engine import TestRun, calculate_pfs


async def compute_pfs(project_id: str, file_path: str, test_name: str) -> float:
    """Real PFS from the last 20 runs of this test; 50.0 when no history exists."""
    pool = get_pool()
    if pool is None:
        return 50.0
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            select r.status, r.duration_ms
            from test_runs r
            join tests t on t.id = r.test_id
            where t.project_id = $1 and t.file_path = $2 and t.test_name = $3
            order by r.created_at desc
            limit 20
            """,
            project_id, file_path, test_name,
        )
    if not rows:
        return 50.0
    runs = [
        TestRun(passed=(r["status"] == "pass"), duration_ms=float(r["duration_ms"] or 0.0))
        for r in reversed(rows)
    ]
    return calculate_pfs(runs).score