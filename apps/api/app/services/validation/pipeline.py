"""Orchestrate branch → commit → trigger → poll → parse. All GitLab I/O lives here."""

import asyncio
import json
import re
import time
from collections.abc import Awaitable, Callable
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.verification import RunResult
from app.services import gitlab_mcp
from app.services.validation.ci_yaml import JOB_PREFIX, generate_ci_yaml

log = get_logger(__name__)
_TERMINAL = {"success", "failed", "canceled", "skipped"}


Emit = Callable[[Any], Awaitable[None]]



async def run_verification(
    *, project_id: str, file_path: str, test_name: str, fixed_source: str,
    branch: str, ref: str, runs: int, emit: Emit, on_heal: Emit,
) -> list[RunResult]:
    """Push the fix + a 5×-run CI config, trigger, poll, return per-run results."""
    s = get_settings()

    if s.validator_dry_run:
        log.info("validator.dry_run", branch=branch)
        return [RunResult(index=i, passed=True, duration_ms=180.0 + i)
                for i in range(1, runs + 1)]

    ci_yaml = generate_ci_yaml(
        file_path=file_path, test_name=test_name, runs=runs, image=s.validator_ci_image)

    await gitlab_mcp.create_branch(project_id, branch, ref)
    await gitlab_mcp.push_files(
        project_id, branch,
        commit_message=f"test: Minari verification harness for {test_name}",
        files=[
            {"file_path": file_path, "content": fixed_source},
            {"file_path": ".gitlab-ci.yml", "content": ci_yaml},
        ],
    )
    pipeline_raw, _ = await gitlab_mcp.trigger_pipeline(project_id, branch)
    pipeline_id = _extract_pipeline_id(pipeline_raw)
    if pipeline_id is None:
        raise RuntimeError("could not determine pipeline id after trigger")

    await _poll_until_terminal(project_id, pipeline_id, emit)

    raw_jobs, _ = await gitlab_mcp.get_pipeline_jobs(project_id, pipeline_id)
    try:
        return _parse_runs(raw_jobs, runs)
    except Exception as exc:                                    # self-heal: malformed jobs
        await on_heal(("parse", f"jobs payload unparseable ({str(exc)[:80]}); retrying"))
        await asyncio.sleep(s.validator_poll_seconds)
        raw_jobs, _ = await gitlab_mcp.get_pipeline_jobs(project_id, pipeline_id)
        return _parse_runs(raw_jobs, runs)                      # second failure ⇒ propagate


async def _poll_until_terminal(project_id: str, pipeline_id: int, emit: Emit) -> None:
    s = get_settings()
    deadline = time.monotonic() + s.validator_timeout_seconds
    while time.monotonic() < deadline:
        raw, _ = await gitlab_mcp.get_pipeline(project_id, pipeline_id)
        status = _extract_status(raw)
        await emit(("poll", status or "pending"))
        if status in _TERMINAL:
            return
        await asyncio.sleep(s.validator_poll_seconds)
    raise TimeoutError(f"pipeline {pipeline_id} did not finish in "
                       f"{s.validator_timeout_seconds}s")


def _as_obj(raw: Any) -> Any:
    if isinstance(raw, dict | list):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def _extract_pipeline_id(raw: Any) -> int | None:
    # create_pipeline returns PROSE, e.g. "Created pipeline #12345 for <ref>.
    # Status: created\nWeb URL: https://.../pipelines/12345". Other tools may
    # return JSON where `id` is an int or a stringified int.
    obj = _as_obj(raw)
    if isinstance(obj, dict):
        pid = obj.get("id")
        if isinstance(pid, int):
            return pid
        if isinstance(pid, str) and pid.isdigit():
            return int(pid)
    m = re.search(r"#(\d+)", str(raw)) or re.search(r"/pipelines/(\d+)", str(raw))
    return int(m.group(1)) if m else None


def _extract_status(raw: Any) -> str | None:
    obj = _as_obj(raw)
    if isinstance(obj, dict) and isinstance(obj.get("status"), str):
        return obj["status"].lower()
    return None


def _parse_runs(raw_jobs: Any, runs: int) -> list[RunResult]:
    obj = _as_obj(raw_jobs)
    jobs = obj if isinstance(obj, list) else (obj.get("jobs") if isinstance(obj, dict) else None)
    if not isinstance(jobs, list):
        raise ValueError("jobs payload is not a list")
    by_name = {j.get("name"): j for j in jobs if isinstance(j, dict)}
    results: list[RunResult] = []
    for i in range(1, runs + 1):
        job = by_name.get(f"{JOB_PREFIX}{i}", {})
        status = str(job.get("status", "")).lower()
        dur = job.get("duration") or 0.0
        results.append(RunResult(
            index=i, passed=(status == "success"), duration_ms=float(dur) * 1000.0))
    return results