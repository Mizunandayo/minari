
"""Best-effort reviewer resolution: blame -> author email -> user id.
NEVER fatal. Any failure falls back to MINARI_DEFAULT_REVIEWER_ID (the token
owner). Returns (reviewer_ids, display_name).
"""



from __future__ import annotations

import re

from app.core.config import get_settings
from app.core.logging import get_logger
from app.services import gitlab_mcp

log = get_logger(__name__)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")




async def resolve_reviewer(
    project_id: str, file_path: str, ref: str,
) -> tuple[list[int], str | None]:
    s = get_settings()
    default = ([s.default_reviewer_id], None) if s.default_reviewer_id else ([], None)
    try:
        blame, _ = await gitlab_mcp.get_git_blame(project_id, file_path, ref)
        m = _EMAIL_RE.search(blame or "")
        if not m:
            return default
        uid, name = await gitlab_mcp.lookup_user(m.group(0))
        if uid is None:
            return default
        return [uid], name
    except Exception as exc:
        log.warning("merger.reviewer.failed", error=str(exc)[:160])
        return default