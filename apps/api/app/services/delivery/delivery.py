"""Open a human facing MR for a verified fix. dry run seam mirrors the Validator."""






from __future__ import annotations

import json
import re

from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.merge import MergeReport
from app.services import gitlab_mcp
from app.services.delivery.confidence import Cascade
from app.services.delivery.reviewer import resolve_reviewer

log = get_logger(__name__)



# @zereight/mcp-gitlab STRINGIFIES every id, so the MR object comes back as
# `"iid": "1"` (quoted), not `"iid": 1` — hence the optional quotes in the regex
# and the str-or-int coercion below (footgun #4: "ids stringified").
_IID_RE = re.compile(r'"iid"\s*:\s*"?(\d+)"?')
_BANG_RE = re.compile(r"!(\d+)")
_URL_RE = re.compile(r"https?://\S+?/merge_requests/\d+")


def _coerce_int(value: object) -> int | None:
    if isinstance(value, bool):           # bool is an int subclass — exclude it
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None





def parse_mr(raw: object) -> tuple[int | None, str | None]:
    """create_merge_request returns JSON OR prose across server versions"""
    try:
        obj = raw if isinstance(raw, dict) else json.loads(str(raw))
        if isinstance(obj, dict):
            iid = _coerce_int(obj.get("iid"))
            url = obj.get("web_url")
            if iid is not None:
                return iid, url if isinstance(url, str) else None
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
    text = str(raw)
    m = _IID_RE.search(text) or _BANG_RE.search(text)
    um = _URL_RE.search(text)
    return (int(m.group(1)) if m else None), (um.group(0) if um else None)





async def deliver_fix(
    *, project_id: str, file_path: str, test_name: str, fixed_source: str,
    mr_branch: str, target_branch: str, title: str, description: str,
    comment: str, labels: list[str], cascade: Cascade, ref: str,
) -> MergeReport:
    s = get_settings()
    report = MergeReport(
        source_branch=mr_branch, target_branch=target_branch, labels=labels,
        detection_confidence=cascade.detection,
        diagnosis_confidence=cascade.diagnosis, fix_confidence=cascade.fix,
        verification_confidence=cascade.verification,
        overall_confidence=cascade.overall,
    )


    # Offline seam: deterministic report, zero gitlab traffic
    if s.merger_dry_run:
        report.mr_iid = 0
        report.mr_url = f"https://gitlab.example/{project_id}/-/merge_requests/0"
        report.assigned_to = "dry-run"
        return report
    

    # 1) clean branch off the target commit only the fixed test file
    await gitlab_mcp.create_branch(project_id, mr_branch, ref=target_branch)
    await gitlab_mcp.push_files(
        project_id, mr_branch, f"fix(flaky): {test_name}",
        [{"file_path": file_path, "content": fixed_source}],
    )


    # 2) reviewer best effort, never fatal
    reviewer_ids, reviewer_name = await resolve_reviewer(project_id, file_path, ref)
    report.assigned_to = reviewer_name or (
        str(reviewer_ids[0]) if reviewer_ids else None)
    


    # 3) open the mr. never merge.
    raw, _ = await gitlab_mcp.create_merge_request(
        project_id, source_branch=mr_branch, target_branch=target_branch,
        title=title, description=description, labels=labels,
        reviewer_ids=reviewer_ids, remove_source_branch=True, squash=True,
    )
    report.mr_iid, report.mr_url = parse_mr(raw)


    
    # 4) attach the verification comment best effort.
    if report.mr_iid is not None:
        try:
            await gitlab_mcp.create_mr_note(project_id, report.mr_iid, comment)
        except Exception as exc:
            log.warning("merger.note.failed", error=str(exc)[:160])

    report.status = "created" if report.mr_iid is not None else "failed"
    return report