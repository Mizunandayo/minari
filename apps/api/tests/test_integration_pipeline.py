"""Dry run integration the graph always reaches a terminal status"""


from __future__ import annotations

import pytest

from app.agents.graph import GRAPH
from app.agents.state import MinariState
from app.core.config import get_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("i", range(20))
async def test_pipeline_reaches_terminal_status(i: int) -> None:
    s = get_settings()
    state = MinariState(
        run_id=f"it-{i}",
        project_id=s.demo_project_id,
        file_path=s.demo_test_file,
        test_name="test_async_result_ready_after_sleep",
    )
    result = await GRAPH.ainvoke(state)
    final = MinariState.model_validate(result)
    assert final.status in {"diagnosed", "fixed", "verified", "delivered",
                            "unverified", "error"}