"""GitLab MCP Server client."""

from __future__ import annotations

import base64
import binascii
import json
import os
import sys
import time
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger(__name__)
_client: MultiServerMCPClient | None = None




def _gitlab_api_url() -> str:
    """GitLab REST API base, e.g. https://gitlab.com/api/v4.

    Accepts the existing ``MINARI_GITLAB_MCP_URL`` whether it ends in ``/mcp``
    (the old hosted-endpoint value) or not — we strip a trailing ``/mcp`` so no
    .env edit is required.
    """
    url = get_settings().gitlab_mcp_url.rstrip("/")
    return url[: -len("/mcp")] if url.endswith("/mcp") else url


def _build_client() -> MultiServerMCPClient:
    settings = get_settings()


    if sys.platform == "win32":
        command, args = "cmd", ["/c", "npx", "-y", "@zereight/mcp-gitlab"]
    else:
        command, args = "minari-mcp", []

    return MultiServerMCPClient(
        {
            "gitlab": {
                "transport": "stdio",
                "command": command,
                "args": args,

                "env": {
                    **os.environ,
                    "GITLAB_PERSONAL_ACCESS_TOKEN": settings.gitlab_token.get_secret_value(),
                    "GITLAB_API_URL": _gitlab_api_url(),
                    # @zereight/mcp-gitlab gates its CI/CD tools (create_pipeline,
                    # get_pipeline, list_pipeline_jobs, ...) behind this flag — the
                    # Validator needs them. Without it they are not exposed.
                    "USE_PIPELINE": "true",
                },
            }
        }
    )






def get_client() -> MultiServerMCPClient:
    global _client
    if _client is None:
        _client = _build_client()
        log.info("mcp.client.created", url=get_settings().gitlab_mcp_url)
    return _client








async def list_tool_names() -> list[str]:
    """Discover available GitLab MCP tools — proves the session is live."""
    tools = await get_client().get_tools()
    names = [t.name for t in tools]
    log.info("mcp.tools.discovered", count=len(names))
    return names






async def ping_mcp() -> bool:
    """Health probe: can we load the tool list?"""
    try:
        names = await list_tool_names()
        return len(names) > 0
    except Exception as exc: 
        log.warning("mcp.ping.failed", error=str(exc))
        return False
    




async def get_file_contents(project_id: str, file_path: str, ref: str = "main") -> Any:

    tools = await get_client().get_tools()
    tool = next((t for t in tools if t.name == "get_file_contents"), None)
    if tool is None:
        available = ", ".join(t.name for t in tools)
        raise RuntimeError(f"'get_file_contents' not exposed. Available: {available}")

    log.info("mcp.call", tool="get_file_contents", project=project_id, path=file_path)
    result = await tool.ainvoke(
        {"project_id": project_id, "file_path": file_path, "ref": ref}
    )
    log.info("mcp.result", tool="get_file_contents", bytes=len(str(result)))
    return result






async def _invoke(tool_name: str, args: dict[str, Any]) -> tuple[Any, int]:
    """Invoke an MCP tool by name; return (result, latency_ms)."""
  
    tools = await get_client().get_tools()
    tool = next((t for t in tools if t.name == tool_name), None)
    if tool is None:
        available = ", ".join(t.name for t in tools)
        raise RuntimeError(f"'{tool_name}' not exposed. Available: {available}")

    log.info("mcp.call", tool=tool_name, args={k: str(v)[:80] for k, v in args.items()})
    started = time.perf_counter()
    result = await tool.ainvoke(args)
    latency_ms = int((time.perf_counter() - started) * 1000)
    log.info("mcp.result", tool=tool_name, bytes=len(str(result)), latency_ms=latency_ms)
    return result, latency_ms





def _extract_file_content(raw: str) -> str:
    """Pull the actual source out of the MCP get_file_contents envelope.

    @zereight/mcp-gitlab returns a JSON object describing the file
    ({file_name, size, encoding, content, ...}) — NOT the raw code. The real
    source lives in `content` (base64 when `encoding == "base64"`, otherwise
    plain text). Returning the whole JSON blob made the Fixer emit non-parseable
    output. Degrades gracefully to the raw string if the shape ever changes.
    """
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return raw
    if not isinstance(obj, dict) or "content" not in obj:
        return raw
    content = obj["content"]
    if not isinstance(content, str):
        return raw
    if obj.get("encoding") == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except (binascii.Error, ValueError):
            return content
    return content


async def get_raw_file(project_id: str, file_path: str, ref: str = "main") -> tuple[str, int]:
    """test source as a text"""
    result, latency = await _invoke(
        "get_file_contents",
        {"project_id": project_id, "file_path": file_path, "ref": ref},
    )
    return _extract_file_content(str(result)), latency










async def get_pipeline_jobs(project_id: str, pipeline_id: int) -> tuple[str, int]:
    """pipeline job logs"""
    for name in ("get_pipeline_jobs", "list_pipeline_jobs"):
        try:
            result, latency = await _invoke(
                name, {"project_id": project_id, "pipeline_id": str(pipeline_id)})
            return str(result), latency
        except RuntimeError:
            continue
    return "", 0










async def search_code(project_id: str, query: str) -> tuple[str, int]:
    """semantic code search for related fixtures utilities"""
    try:
        result, latency = await _invoke(
            "search_repository_code", {"project_id": project_id, "search": query}
        )
        return str(result), latency
    except RuntimeError:
        return "", 0
    






async def get_git_blame(project_id: str, file_path: str, ref: str = "main") -> tuple[str, int]:
    """last modifier context"""
    for name in ("get_file_blame", "list_commits"):
        try:
            args = {"project_id": project_id, "file_path": file_path, "ref": ref} \
                if name == "get_file_blame" else {"project_id": project_id, "path": file_path}
            result, latency = await _invoke(name, args)
            return str(result), latency
        except RuntimeError:
            continue
    return "", 0
    





async def create_branch(project_id: str, branch: str, ref: str = "main") -> tuple[Any, int]:
    """Create a fix branch off `ref`. Idempotent-ish: a 'already exists' is tolerated."""
    try:
        return await _invoke("create_branch",
                             {"project_id": project_id, "branch": branch, "ref": ref})
    except RuntimeError:
        return await _invoke("create_branch",
                             {"project_id": project_id, "branch": branch, "ref_name": ref})


async def push_files(
    project_id: str, branch: str, commit_message: str, files: list[dict[str, str]],
) -> tuple[Any, int]:
    """Commit each file via create_or_update_file (an UPSERT).

    `files` = [{"file_path": ..., "content": ...}, ...]

    The MCP `push_files` tool uses create-only commit actions and the GitLab API
    400s with "A file with this name already exists" when the path already exists
    (our case — we rewrite an existing test file and overwrite .gitlab-ci.yml).
    create_or_update_file updates an existing file cleanly, so we loop it (one
    commit per file; the final branch state is what the triggered pipeline reads).
    """
    last: tuple[Any, int] = ("", 0)
    for f in files:
        last = await _invoke("create_or_update_file", {
            "project_id": project_id, "branch": branch,
            "file_path": f["file_path"], "content": f["content"],
            "commit_message": commit_message,
        })
    return last


async def trigger_pipeline(project_id: str, ref: str) -> tuple[Any, int]:
    """Start a pipeline on `ref` (runs the .gitlab-ci.yml committed to that branch)."""
    for name in ("create_pipeline", "trigger_pipeline", "run_pipeline"):
        try:
            return await _invoke(name, {"project_id": project_id, "ref": ref})
        except RuntimeError:
            continue
    raise RuntimeError("no pipeline-trigger tool exposed by the MCP server")


async def get_pipeline(project_id: str, pipeline_id: int) -> tuple[Any, int]:
    for name in ("get_pipeline", "get_pipeline_status"):
        try:
            return await _invoke(
                name, {"project_id": project_id, "pipeline_id": str(pipeline_id)})
        except RuntimeError:
            continue
    return "", 0


async def create_issue(
    project_id: str, title: str, description: str, labels: list[str] | None = None,
) -> tuple[Any, int]:
    """Human-handoff fallback when the gate ultimately fails."""
    args: dict[str, Any] = {"project_id": project_id, "title": title,
                            "description": description}
    if labels:
        args["labels"] = labels        # schema expects an array of label names
    return await _invoke("create_issue", args)
