"""Day-5 E2E driver: POST /diagnose for each demo test, follow the SSE stream,
classify the terminal outcome. Run from apps/api with the server up on :8000.
uv run python ../../scripts/e2e_all_tests.py
"""

from __future__ import annotations
import asyncio
import json
import os
import httpx




BASE = os.environ.get("MINARI_E2E_BASE", "http://localhost:8000")
KEY = os.environ["MINARI_DEMO_API_KEY"]
PROJECT = os.environ["MINARI_DEMO_PROJECT_ID"]





# (file_path, real pytest function name) — must be REAL node ids (footgun #5).
# 5 files x 2 tests = 10, one pair per root-cause category. Verified against the
# demo repo clone (C:\Users\trist\Desktop\Programming\flakytests).
DEMO_TESTS: list[tuple[str, str]] = [
    # async
    ("tests/test_async_timing.py", "test_async_result_ready_after_sleep"),
    ("tests/test_async_timing.py", "test_async_polling_timeout_too_tight"),
    # data isolation
    ("tests/test_data_isolation.py", "test_checkout_items_count"),
    ("tests/test_data_isolation.py", "test_cart_total_isolation"),
    # network
    ("tests/test_network_deps.py", "test_fetch_items_from_service"),
    ("tests/test_network_deps.py", "test_service_responds_within_latency_budget"),
    # race
    ("tests/test_race_conditions.py", "test_concurrent_counter_increment"),
    ("tests/test_race_conditions.py", "test_event_order_dependent_result"),
    # resource contention
    ("tests/test_resource_contention.py", "test_pool_acquire_under_contention"),
    ("tests/test_resource_contention.py", "test_memory_buffer_within_budget"),
]





async def run_one(client: httpx.AsyncClient, file_path: str, test_name: str) -> str:
    r = await client.post(f"{BASE}/api/v1/diagnose",
                          headers={"X-API-Key": KEY, "Content-Type": "application/json"},
                          json={"project_id": PROJECT, "file_path": file_path,
                                "test_name": test_name})
    r.raise_for_status()
    acc = r.json()
    outcome = "no-terminal-event"
    url = f"{BASE}{acc['stream_path']}?token={acc['stream_token']}"
    async with client.stream("GET", url, timeout=600) as s:
        event_type = None
        async for line in s.aiter_lines():
            if line.startswith("event:"):
                event_type = line.split(":", 1)[1].strip()
            elif line.startswith("data:") and event_type == "merge":
                data = json.loads(line[5:].strip())
                outcome = f"MR !{data.get('mr_iid')}" if data.get("mr_iid") is not None else "merge-no-iid"
            elif line.startswith("data:") and event_type in ("done", "error"):
                outcome = outcome if outcome.startswith("MR") else f"{event_type}"
                break
    return outcome




async def main() -> None:
    async with httpx.AsyncClient() as client:
        results: list[tuple[str, str]] = []
        for fp, tn in DEMO_TESTS:
            try:
                out = await run_one(client, fp, tn)
            except Exception as exc:  # noqa: BLE001 - report, don't abort the suite
                out = f"error: {str(exc)[:80]}"
            results.append((tn, out))
            print(f"  {tn:<48} -> {out}")
        mrs = sum(1 for _, o in results if o.startswith("MR"))
        print(f"\n{mrs}/{len(results)} produced merge requests "
              f"(checkpoint target: 8/10).")


if __name__ == "__main__":
    asyncio.run(main())