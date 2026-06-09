"""dashboard aggregations pure reads over the real supabase tables."""


from __future__ import annotations

from datetime import date, timedelta

from app.db.session import get_pool

_TREND_DAYS = 30




async def fetch_summary(project_id: str) -> dict:
    pool = get_pool()
    if pool is None:
        return _empty_summary()
    async with pool.acquire() as conn:
        # Tests delivered as REAL MRs (iid > 0 — excludes dry-run/orphaned 0-iid rows),
        # with a 7-day window count.
        mr = await conn.fetchrow(
            """
            select count(*) as total,
                   count(*) filter (where mr.created_at >= now() - interval '7 days') as week
            from merge_requests mr
            join verifications v on v.id = mr.verification_id
            join fixes f        on f.id = v.fix_id
            join diagnoses d    on d.id = f.diagnosis_id
            join tests t        on t.id = d.test_id
            where t.project_id = $1
              and mr.gitlab_mr_iid is not null
              and mr.gitlab_mr_iid > 0
            """,
            project_id,
        )
       # Gate pass-rate across verifications for this project.
        ver = await conn.fetchrow(
            """
            select count(*) as total,
                   count(*) filter (where v.gate_passed) as passed
            from verifications v
            join fixes f     on f.id = v.fix_id
            join diagnoses d on d.id = f.diagnosis_id
            join tests t     on t.id = d.test_id
            where t.project_id = $1
            """,
            project_id,
        )
        # Flakiness = CURRENT fail-rate of the last 7 days of test_runs, so the headline
        # matches the right edge of the trend chart (same data source, no PFS-50 cap).
        flak = await conn.fetchrow(
            """
            select count(*) filter (where tr.status in ('fail','error'))::float
                       / nullif(count(*), 0) as rate
            from test_runs tr
            join tests t on t.id = tr.test_id
            where t.project_id = $1
              and tr.created_at >= now() - interval '7 days'
            """,
            project_id,
        )
        # Agent diagnosis latency (Gemini call time) recorded on the diagnoses row.
        lat = await conn.fetchrow(
            """
            select avg(d.latency_ms) as avg_latency
            from diagnoses d
            join tests t on t.id = d.test_id
            where t.project_id = $1 and d.latency_ms is not null
            """,
            project_id,
        )



    total_ver = int(ver["total"] or 0)
    return {
        "tests_fixed": int(mr["total"] or 0),
        "fixed_this_week": int(mr["week"] or 0),
        "success_rate": (int(ver["passed"] or 0) / total_ver) if total_ver else 0.0,
        "flakiness_rate": float(flak["rate"]) if flak["rate"] is not None else 0.0,
        "avg_fix_latency_ms": int(lat["avg_latency"] or 0),
        "verifications_total": total_ver,
    }





async def fetch_trends(project_id: str) -> list[dict]:
    """Daily flakiness = fail-rate of test_runs, over the last 30 days (dense, zero-filled)."""
    pool = get_pool()
    start = date.today() - timedelta(days=_TREND_DAYS - 1)
    buckets: dict[str, dict] = {
        (start + timedelta(days=i)).isoformat(): {"fail": 0, "total": 0}
        for i in range(_TREND_DAYS)
    }
    if pool is not None:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                select to_char(tr.created_at, 'YYYY-MM-DD') as day,
                       count(*) as total,
                       count(*) filter (where tr.status in ('fail','error')) as fail
                from test_runs tr
                join tests t on t.id = tr.test_id
                where t.project_id = $1
                  and tr.created_at >= now() - interval '30 days'
                group by 1
                """,
                project_id,
            )
        for r in rows:
            if r["day"] in buckets:
                buckets[r["day"]] = {"fail": int(r["fail"]), "total": int(r["total"])}

    return [
        {
            "day": day,
            "flakiness_rate": (b["fail"] / b["total"]) if b["total"] else 0.0,
            "runs": b["total"],
        }
        for day, b in sorted(buckets.items())
    ]







async def fetch_root_causes(project_id: str) -> list[dict]:
    pool = get_pool()
    if pool is None:
        return []
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            with latest as (
                select distinct on (d.test_id) d.category
                from diagnoses d
                join tests t on t.id = d.test_id
                where t.project_id = $1 and d.category is not null
                order by d.test_id, d.created_at desc
            )
            select category, count(*) as count
            from latest group by category order by count desc
            """,
            project_id,
        )
    return [{"category": r["category"], "count": int(r["count"])} for r in rows]









async def fetch_activity(project_id: str, limit: int = 10) -> list[dict]:
    pool = get_pool()
    if pool is None:
        return []
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            select t.test_name, t.file_path, d.category, d.confidence,
                   mr.gitlab_mr_iid as mr_iid, mr.gitlab_mr_url as mr_url,
                   mr.created_at
            from merge_requests mr
            join verifications v on v.id = mr.verification_id
            join fixes f        on f.id = v.fix_id
            join diagnoses d    on d.id = f.diagnosis_id
            join tests t        on t.id = d.test_id
            where t.project_id = $1
              and mr.gitlab_mr_iid is not null
              and mr.gitlab_mr_iid > 0
            order by mr.created_at desc
            limit $2
            """,
            project_id, limit,
        )
    return [
        {
            "test_name": r["test_name"],
            "file_path": r["file_path"],
            "category": r["category"],
            "confidence": float(r["confidence"]) if r["confidence"] is not None else None,
            "mr_iid": int(r["mr_iid"]) if r["mr_iid"] is not None else None,
            "mr_url": r["mr_url"],
            "created_at": r["created_at"].isoformat(),
        }
        for r in rows
    ]




def _empty_summary() -> dict:
    return {
        "tests_fixed": 0, "fixed_this_week": 0, "success_rate": 0.0,
        "flakiness_rate": 0.0, "avg_fix_latency_ms": 0, "verifications_total": 0,
    }