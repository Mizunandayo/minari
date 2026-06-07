from __future__ import annotations

import time

from app.agents.events import RUNS, DecideEvent, MCPCallEvent, MergeEvent
from app.agents.state import MinariState
from app.core.config import get_settings
from app.core.logging import get_logger
from app.services.delivery.confidence import cascade_confidence
from app.services.delivery.delivery import deliver_fix
from app.services.delivery.mr_description import (
    build_mr_description,
    build_mr_title,
    build_verification_comment,
    mr_labels,
)
from app.services.validation.branch import (
    is_safe_node_name,
    is_safe_repo_path,
    safe_slug,
)

log = get_logger(__name__)





def _pipeline_url(project_id: str, pipeline_id: int | None) -> str | None:
    if pipeline_id is None or "/" not in project_id:
        return None
    return f"https://gitlab.com/{project_id}/-/pipelines/{pipeline_id}"





async def merger_node(state: MinariState) -> MinariState:
    bus = RUNS.get(state.run_id)
    s = get_settings()

    async def emit(event) -> None:
        if bus is not None:
            await bus.emit(event)

    # Preconditions — defense in depth (the edge already gated on these).
    v = state.verification
    if state.status != "verified" or v is None or not v.gate_passed:
        return state
    if state.diagnosis is None or state.fixes is None:
        return state
    if state.project_id not in s.write_allowlist:
        await emit(DecideEvent(stage="merger",
                               text="Project not on the allow-list - refusing to open an MR."))
        return state
    if not (is_safe_repo_path(state.file_path) and is_safe_node_name(state.test_name)):
        await emit(DecideEvent(stage="merger",
                               text="Path/name failed safety validation - refusing to open an MR."))
        return state

    chosen = next((c for c in state.fixes.candidates if c.rank == v.chosen_rank), None)
    if chosen is None:
        await emit(DecideEvent(stage="merger",
                               text="Winning candidate not found - skipping delivery."))
        return state

    cascade = cascade_confidence(
        pfs_score=state.pfs_score,
        diagnosis_confidence=state.diagnosis.confidence,
        fix_confidence=chosen.confidence,
        pass_rate=v.pass_rate,
    )

    title = build_mr_title(state.test_name, state.diagnosis.category.value)
    labels = mr_labels(state.diagnosis.category.value)
    description = build_mr_description(
        diagnosis=state.diagnosis, fix=chosen, verification=v, cascade=cascade,
        test_name=state.test_name, file_path=state.file_path,
        pfs_score=state.pfs_score,
        pipeline_url=_pipeline_url(state.project_id, v.pipeline_id),
    )
    comment = build_verification_comment(v, cascade)
    mr_branch = f"minari/mr-{safe_slug(state.test_name)}-{state.run_id[:8]}"

    await emit(DecideEvent(
        stage="merger",
        text=f"Opening MR from clean branch '{mr_branch}' "
             f"(overall confidence {cascade.overall * 100:.0f}%, {cascade.tier})."))
    await emit(MCPCallEvent(stage="merger", tool="gitlab.create_merge_request",
                            params_summary=title))

    started = time.perf_counter()
    try:
        report = await deliver_fix(
            project_id=state.project_id, file_path=state.file_path,
            test_name=state.test_name, fixed_source=chosen.fixed_source,
            mr_branch=mr_branch, target_branch=s.mr_target_branch,
            title=title, description=description, comment=comment,
            labels=labels, cascade=cascade, ref=state.ref,
        )
    except Exception as exc:
        log.error("merger.failed", run_id=state.run_id, error=str(exc)[:200])
        await emit(DecideEvent(
            stage="merger",
            text=f"MR creation failed: {str(exc)[:140]}. Fix is verified on "
                 f"'{v.branch_name}' for a manual MR."))
        return state 

    state.merge = report
    if report.status == "created":
        state.status = "delivered"
        await emit(MergeEvent(
            stage="merger", mr_iid=report.mr_iid, mr_url=report.mr_url,
            assigned_to=report.assigned_to,
            detection_confidence=cascade.detection,
            diagnosis_confidence=cascade.diagnosis,
            fix_confidence=cascade.fix,
            verification_confidence=cascade.verification,
            overall_confidence=cascade.overall))
        log.info("merger.delivered", run_id=state.run_id, mr_iid=report.mr_iid,
                 ms=int((time.perf_counter() - started) * 1000))
    else:
        await emit(DecideEvent(
            stage="merger",
            text="MR endpoint returned no iid - left the fix on the verified branch."))
    return state


    

    


