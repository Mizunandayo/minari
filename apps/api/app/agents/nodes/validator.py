from __future__ import annotations

import time

from app.agents.events import (
    RUNS,
    DecideEvent,
    HealEvent,
    MCPCallEvent,
    ReasonEvent,
    VerifyEvent,
)
from app.agents.state import MinariState
from app.core.config import get_settings
from app.core.logging import get_logger
from app.repositories.test_runs_repo import recent_durations
from app.schemas.verification import VerificationReport
from app.services import gitlab_mcp
from app.services.validation.branch import (
    fix_branch_name,
    is_safe_node_name,
    is_safe_repo_path,
)
from app.services.validation.gate import evaluate_gate
from app.services.validation.pipeline import run_verification

log = get_logger(__name__)




async def validator_node(state: MinariState) -> MinariState:
    bus = RUNS.get(state.run_id)
    s = get_settings()

    async def emit(event) -> None:
        if bus is not None:
            await bus.emit(event)

    # Preconditions
    if state.fixes is None or not state.fixes.candidates:
        await emit(DecideEvent(stage="validator",
                               text="No safe fix to verify — skipping verification."))
        return state

    if state.project_id not in s.write_allowlist:            
        await emit(DecideEvent(
            stage="validator",
            text="Project is not on the verification allow-list — refusing to "
                 "branch, push, or trigger CI. Handing off for manual review."))
        state.status = "unverified"
        return state

    if not (is_safe_repo_path(state.file_path) and is_safe_node_name(state.test_name)):
        await emit(DecideEvent(
            stage="validator",
            text="Test path or name failed safety validation — refusing to write "
                 "to the repository."))
        state.status = "unverified"
        return state

    candidates = list(state.fixes.candidates)                  
    baseline = await recent_durations(
        state.project_id, state.file_path, state.test_name)
    base_branch = fix_branch_name(state.test_name, state.run_id)
    started = time.perf_counter()

    report = VerificationReport(branch_name=base_branch)
    max_attempts = min(len(candidates), s.validator_max_heals + 1)

    # Verify→heal loop over the already-generated candidates
    for attempt in range(max_attempts):
        candidate = candidates[attempt]
        # A unique branch per candidate — otherwise the 2nd/3rd heal hits
        # "Branch already exists" on the branch the 1st attempt created.
        branch = f"{base_branch}-c{candidate.rank}"
        report.chosen_rank = candidate.rank
        report.branch_name = branch
        report.healing_attempts = attempt

        if attempt > 0:
            await emit(HealEvent(stage="validator", attempt=attempt,
                                 reason=f"Gate failed — verifying candidate "
                                        f"#{candidate.rank} instead."))

        await emit(DecideEvent(
            stage="validator",
            text=f"Verifying candidate #{candidate.rank}: branch '{branch}', "
                 f"{s.validator_runs} isolated CI runs."))
        await emit(MCPCallEvent(stage="validator", tool="gitlab.create_branch",
                                params_summary=branch))

        async def on_poll(payload) -> None:
            await emit(ReasonEvent(stage="validator",
                                   text=f"Pipeline status: {payload[1]}"))

        async def on_heal(payload, _attempt: int = attempt) -> None:
            await emit(HealEvent(stage="validator", attempt=_attempt,
                                 reason=str(payload[1])))

        try:
            runs = await run_verification(
                project_id=state.project_id, file_path=state.file_path,
                test_name=state.test_name, fixed_source=candidate.fixed_source,
                branch=branch, ref=state.ref, runs=s.validator_runs,
                emit=on_poll, on_heal=on_heal,
            )
        except Exception as exc:                                 
            log.warning("validator.attempt.failed", run_id=state.run_id,
                        attempt=attempt, error=str(exc)[:200])
            await emit(HealEvent(stage="validator", attempt=attempt,
                                 reason=f"Verification run errored: {str(exc)[:120]}"))
            continue

        gate = evaluate_gate(
            runs=runs, expected_runs=s.validator_runs, baseline_durations=baseline,
            min_variance_reduction=s.validator_variance_reduction_min,
            runtime_tolerance=s.validator_runtime_tolerance,
        )
        report.run_results = runs
        report.pass_rate = gate.pass_rate
        report.variance_before = gate.variance_before
        report.variance_after = gate.variance_after
        report.variance_reduction_pct = gate.variance_reduction_pct
        report.gate_passed = gate.passed

        for r in runs:
            await emit(VerifyEvent(
                stage="validator", run_index=r.index, total_runs=s.validator_runs,
                passed=r.passed, duration_ms=r.duration_ms, gate_passed=gate.passed,
                variance_reduction_pct=gate.variance_reduction_pct))

        if gate.passed:
            await emit(DecideEvent(stage="validator",
                                   text=f"SAFETY GATE PASSED — {gate.reason}."))
            state.verification = report
            state.status = "verified"
            log.info("validator.passed", run_id=state.run_id, rank=candidate.rank,
                     ms=int((time.perf_counter() - started) * 1000))
            return state

        await emit(DecideEvent(stage="validator",
                               text=f"Gate failed for candidate #{candidate.rank}: "
                                    f"{gate.reason}."))

    # Exhausted: file an issue with full context
    await emit(DecideEvent(
        stage="validator",
        text="All candidates failed verification — filing a GitLab issue for a human."))
    issue_url = await _file_fallback_issue(state, report, emit)
    report.issue_url = issue_url
    state.verification = report
    state.status = "unverified"
    log.info("validator.exhausted", run_id=state.run_id,
             attempts=report.healing_attempts + 1)
    return state




async def _file_fallback_issue(state, report, emit) -> str | None:
    diag = state.diagnosis
    title = f"[Minari] Flaky test needs manual review: {state.test_name}"
    body = (
        f"Minari diagnosed **{state.test_name}** "
        f"(`{state.file_path}`) but could not produce a verified fix.\n\n"
        f"**Root cause:** {diag.category.value if diag else 'unknown'} "
        f"(confidence {diag.confidence if diag else 0:.2f})\n"
        f"**Verification:** {report.summary}\n"
        f"**Branch with attempted fixes:** `{report.branch_name}`\n\n"
        f"Generated by Minari — please review the branch and the diagnosis above."
    )
    try:
        await emit(MCPCallEvent(stage="validator", tool="gitlab.create_issue",
                                params_summary=title))
        raw, _ = await gitlab_mcp.create_issue(
            state.project_id, title, body, labels=["minari:needs-review", "flaky-test"])
        import json as _json
        obj = raw if isinstance(raw, dict) else _json.loads(str(raw))
        return obj.get("web_url") if isinstance(obj, dict) else None
    except Exception as exc:
        log.warning("validator.issue.failed", error=str(exc)[:200])
        return None