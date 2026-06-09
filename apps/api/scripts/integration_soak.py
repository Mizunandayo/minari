"""Run the full pipeline n times in dry run mode"""



from __future__ import annotations

import asyncio
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agents.graph import GRAPH
from app.agents.state import MinariState
from app.core.config import get_settings
from app.db.session import init_pool


async def main(n: int) -> None:
    await init_pool()
    s = get_settings()
    statuses: Counter[str] = Counter()
    failures = 0
    for i in range(n):
        state = MinariState(
            run_id=f"soak-{i}",
            project_id=s.demo_project_id,
            file_path=s.demo_test_file,
            test_name="test_async_result_ready_after_sleep",
        )
        try:
            result = await GRAPH.ainvoke(state)
            final = MinariState.model_validate(result)
            statuses[final.status or "unknown"] += 1
        except Exception as exc: 
            failures += 1
            print(f"  run {i}: UNCAUGHT {type(exc).__name__}: {exc}")
    print(f"\nSoak complete: {n} runs")
    print(f"  status distribution: {dict(statuses)}")
    print(f"  uncaught exceptions: {failures}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 20))