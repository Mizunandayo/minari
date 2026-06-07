"""Persist delivered mrs to the existing merge_requests table"""



from __future__ import annotations

from app.db.session import get_pool
from app.schemas.merge import MergeReport


async def create_merge_request_record(
    verification_id: str, report: MergeReport,
) -> str | None:
    pool = get_pool()
    if pool is None or report.mr_iid is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            insert into merge_requests
              (verification_id, gitlab_mr_iid, gitlab_mr_url,
               overall_confidence, assigned_to, status)
            values ($1, $2, $3, $4, $5, $6)
            returning id
            """,
            verification_id, report.mr_iid, report.mr_url,
            round(report.overall_confidence, 3),   # column is numeric(4,3)
            report.assigned_to, "created",
        )
    return str(row["id"]) if row else None
