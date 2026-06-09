from __future__ import annotations

import pytest

from app.mcp_server import tools


@pytest.mark.asyncio
async def test_unknown_project_is_refused() -> None:
    with pytest.raises(tools.ToolError):
        await tools.detect("attacker/owned-repo", "tests/x.py", "test_x")


@pytest.mark.asyncio
async def test_verify_defaults_to_dry_run() -> None:
    from app.core.config import get_settings
    res = await tools.verify(get_settings().demo_project_id, "tests/x.py", "test_x")
    assert res["executed"] is False
    assert res["mode"] in {"dry-run", "redirect"}
