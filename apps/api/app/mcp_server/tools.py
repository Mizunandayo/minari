"""validated tool implementations for the Minari MCP Server"""



from __future__ import annotations

from typing import Any

from app.agents.state import MinariState
from app.core.config import get_settings
from app.core.logging import get_logger
from app.repositories.test_runs_repo import compute_pfs
from app.services.gitlab_mcp import get_raw_file
from app.services.llm.fixer import generate_fixes

log = get_logger("minari.mcp")



class ToolError(Exception):
   """Raised for invalid/forbidden tool input surfaced as clean mcp error"""


def _require_known_project(project_id: str) -> None:
    """A caller may only target a project Minari already knows about."""
    s = get_settings()
    allowed = set(s.allowed_project_ids) | {s.demo_project_id}
    if project_id not in allowed:
        raise ToolError(
            f"project_id '{project_id}' is not in the Minari allow-list. "
            "Refusing to operate on an unknown project."
        )
    


def _require_str(name: str, value: Any, *, max_len: int = 300) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"'{name}' must be a non-empty string.")
    if len(value) > max_len:
        raise ToolError(f"'{name}' exceeds {max_len} characters.")
    return value.strip()




async def detect(project_id: str, file_path: str, test_name: str) -> dict:
    """READ ONLY probabilistic flakiness score from run history"""
    _require_known_project(project_id)
    file_path = _require_str("file_path", file_path)
    test_name = _require_str("test_name", test_name)
    score = await compute_pfs(project_id, file_path, test_name)
    verdict = "flaky" if score > 85 else "not_flaky" if score < 20 else "uncertain"
    return {"pfs_score": score, "verdict": verdict, "test_name": test_name}




async def diagnose(project_id: str, file_path: str, test_name: str) -> dict:
    """Read only reads source via mcp runs the detective node only"""
    from app.agents.nodes.detective import detective_node

    _require_known_project(project_id)
    file_path = _require_str("file_path", file_path)
    test_name = _require_str("test_name", test_name)
    state = MinariState(
        run_id="mcp-diagnose",
        project_id=project_id,
        file_path=file_path,
        test_name=test_name,
    )
    result = await detective_node(state)
    final = MinariState.model_validate(result)
    if final.diagnosis is None:
        return {"diagnosed": False, "reason": final.error or "insufficient evidence"}
    d = final.diagnosis
    return {
        "diagnosed": True,
        "category": d.category.value,
        "confidence": d.confidence,
        "recommended_fix_category": d.recommended_fix_category,
        "reasoning": [s.observation for s in d.reasoning_chain],
    }





async def fix(project_id: str, file_path: str, test_name: str) -> dict:
    """read only no gitlab writes diagnose then generate ranked candidate diffs."""
    diag = await diagnose(project_id, file_path, test_name)
    if not diag.get("diagnosed"):
        return {"fixed": False, "reason": diag.get("reason", "diagnosis failed")}
    source = await get_raw_file(project_id, file_path)
    s = get_settings()
    drafts, _ms = await generate_fixes(
        model=s.gemini_flash_model,
        category=diag["category"],
        source=source,
        file_path=file_path,
        test_name=test_name,
    )
    return {
        "fixed": True,
        "category": diag["category"],
        "candidates": [
            {"rank": c.rank, "fix_category": c.fix_category,
             "confidence": c.confidence, "explanation": c.explanation}
            for c in drafts.candidates
        ],
    }





async def verify(project_id: str, file_path: str, test_name: str) -> dict:
    """write tool hard gated. touches gitlab only when allowed"""
    s = get_settings()
    _require_known_project(project_id)
    if not s.mcp_allow_writes or project_id not in s.write_allowlist:
        log.warning("mcp.verify.refused", project_id=project_id,
                    allow_writes=s.mcp_allow_writes)
        return {
            "executed": False,
            "mode": "dry-run",
            "reason": ("Write operations are disabled. Set MINARI_MCP_ALLOW_WRITES=true "
                       "and add the project to MINARI_ALLOWED_PROJECT_IDS to enable."),
            "plan": ["create isolated branch", "commit rewritten test",
                     "run 5× CI", "evaluate safety gate"],
        }
    return {
        "executed": False,
        "mode": "redirect",
        "reason": "Live verification runs through the authenticated HTTP pipeline.",
        "endpoint": "POST /api/v1/diagnose",
    }
