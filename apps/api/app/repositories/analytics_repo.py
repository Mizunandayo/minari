"""read models for predictive forecasting and sustainability."""



from __future__ import annotations

from app.db.session import get_pool

_HISTORY_DAYS = 30




async def fetch_test_daily_history(project_id: str) -> dict[str, list[dict]]:
    """{ "<file_path>::<test_name>": [ {day, fail, total}, ... ] } over 30 days.

    Sorted ascending by day per test. Tests with no runs in the window are absent
    (the forecaster treats "absent" as "insufficient history", not "zero risk").
    """
    pool = get_pool()
    if pool is None:
        return {}
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            select t.file_path, t.test_name,
                   to_char(tr.created_at, 'YYYY-MM-DD') as day,
                   count(*) as total,
                   count(*) filter (where tr.status in ('fail','error')) as fail
            from test_runs tr
            join tests t on t.id = tr.test_id
            where t.project_id = $1
              and tr.created_at >= now() - interval '30 days'
            group by t.file_path, t.test_name, day
            order by t.file_path, t.test_name, day
            """,
            project_id,
        )
    history: dict[str, list[dict]] = {}
    for r in rows:
        key = f"{r['file_path']}::{r['test_name']}"
        history.setdefault(key, []).append(
            {"day": r["day"], "fail": int(r["fail"]), "total": int(r["total"])}
        )
    return history






async def fetch_savings_inputs(project_id: str) -> dict:
    """Counts that drive the carbon estimate — all REAL rows for this project."""
    pool = get_pool()
    if pool is None:
        return {"verifications_passed": 0, "runs_per_verification": 0, "tests_fixed": 0}
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            select
              count(*) filter (where v.gate_passed) as verifications_passed,
              coalesce(avg((select count(*) from jsonb_array_elements(v.run_results))), 0)
                  as runs_per_verification
            from verifications v
            join fixes f     on f.id = v.fix_id
            join diagnoses d on d.id = f.diagnosis_id
            join tests t     on t.id = d.test_id
            where t.project_id = $1
            """,
            project_id,
        )
        mr = await conn.fetchrow(
            """
            select count(*) as tests_fixed
            from merge_requests mr
            join verifications v on v.id = mr.verification_id
            join fixes f     on f.id = v.fix_id
            join diagnoses d on d.id = f.diagnosis_id
            join tests t     on t.id = d.test_id
            where t.project_id = $1 and mr.gitlab_mr_iid > 0
            """,
            project_id,
        )
    return {
        "verifications_passed": int(row["verifications_passed"] or 0),
        "runs_per_verification": float(row["runs_per_verification"] or 0.0),
        "tests_fixed": int(mr["tests_fixed"] or 0),
    }