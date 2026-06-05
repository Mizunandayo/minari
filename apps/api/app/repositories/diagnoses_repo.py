"""Diagnosis run lifecycle + final result persistence."""



from __future__ import annotations

import json

from app.db.session import get_pool
from app.schemas.diagnosis import Diagnosis


async def create_run(*, run_id: str, project_id: str, file_path: str, test_name: str) -> None:
    pool = get_pool()
    if pool is None:
        return
    async with pool.acquire() as conn:
        await conn.execute(
            """insert into diagnosis_runs (id, project_id, file_path, test_name, status)
               values ($1, $2, $3, $4, 'running')
               on conflict (id) do nothing""",
            run_id, project_id, file_path, test_name,
        )







async def finalize_run(
    *, run_id: str, test_id: str | None, status: str, pfs_score: float,
    model_used: str, diagnosis: Diagnosis | None, latency_ms: int, error: str | None,
) -> str | None:                                
    pool = get_pool()
    if pool is None:
        return None                                 
    async with pool.acquire() as conn:
        diagnosis_id = None
        if diagnosis is not None and test_id is not None:
            diag_row = await conn.fetchrow(
                """insert into diagnoses
                   (test_id, pfs_score, category, confidence, reasoning_chain,
                    triggering_lines, model_used, latency_ms)
                   values ($1,$2,$3,$4,$5,$6,$7,$8) returning id""",
                test_id, pfs_score, diagnosis.category.value, diagnosis.confidence,
                json.dumps([s.model_dump() for s in diagnosis.reasoning_chain]),
                diagnosis.triggering_lines, model_used, latency_ms,
            )
            diagnosis_id = diag_row["id"]
        await conn.execute(
            """update diagnosis_runs
               set status=$2, pfs_score=$3, model_used=$4, diagnosis_id=$5,
                   latency_ms=$6, error=$7, updated_at=now()
               where id=$1""",
            run_id, status, pfs_score, model_used, diagnosis_id, latency_ms, error,
        )
        return str(diagnosis_id) if diagnosis_id is not None else None   