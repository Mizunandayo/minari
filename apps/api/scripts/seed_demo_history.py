"""Seed real test_runs history so dashboard/trends shows a declining curve"""



from __future__ import annotations

import asyncio
import os
import random
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Make `app` importable when run as a standalone script (apps/api on sys.path).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402
from app.db.session import get_pool, init_pool  # noqa: E402

_DAYS = 30
_RUNS_PER_DAY = 8
_SEED_RUNNER = "minari-seed"        
_BASELINE = datetime.now(UTC).replace(hour=12, minute=0, second=0, microsecond=0)





async def main() -> None:
    if os.getenv("MINARI_ALLOW_SEED", "").lower() != "true":
        raise SystemExit("Refusing to seed: set MINARI_ALLOW_SEED=true to confirm.")


    await init_pool()
    pool = get_pool()
    if pool is None:
        raise SystemExit("No DB pool — check apps/api/.env DB URL.")

    project_id = get_settings().demo_project_id
    rng = random.Random(42)  # noqa: S311 - demo seed data, not cryptographic

    async with pool.acquire() as conn:
        tests = await conn.fetch(
            "select id from tests where project_id = $1", project_id,
        )
        if not tests:
            raise SystemExit("No tests for project — run the pipeline once first.")

        await conn.execute(
            "delete from test_runs where runner_id = $1", _SEED_RUNNER,
        )

        rows: list[tuple] = []
        for day in range(_DAYS):
            # Fail probability decays 0.42 -> ~0.04 across the window (Minari fixing tests).
            progress = day / (_DAYS - 1)
            fail_p = max(0.04, 0.42 * (1.0 - progress))
            ts = _BASELINE - timedelta(days=_DAYS - 1 - day)
            for t in tests:
                for _ in range(_RUNS_PER_DAY):
                    failed = rng.random() < fail_p
                    rows.append((
                        t["id"],
                        "fail" if failed else "pass",
                        rng.randint(120, 480),                  # duration_ms
                        _SEED_RUNNER,
                        ts + timedelta(minutes=rng.randint(0, 600)),
                    ))

        await conn.executemany(
            """
            insert into test_runs (test_id, status, duration_ms, runner_id, created_at)
            values ($1, $2, $3, $4, $5)
            """,
            rows,
        )
    print(f"Seeded {len(rows)} test_runs across {_DAYS} days for {len(tests)} tests.")


if __name__ == "__main__":
    asyncio.run(main())