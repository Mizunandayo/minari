"""GitLab MCP Server client."""

from __future__ import annotations

import os
import sys
from typing import Any
import time
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











async def get_raw_file(project_id: str, file_path: str, ref: str = "main") -> tuple[str, int]:
    """test source as a text"""
    result, latency = await _invoke(
        "get_file_contents",
        {"project_id": project_id, "file_path": file_path, "ref": ref},
    )
    return str(result), latency










async def get_pipeline_jobs(project_id: str, pipeline_id: int) -> tuple[str, int]:
    """pipeline job logs"""
    for name in ("get_pipeline_jobs", "list_pipeline_jobs"):
        try:
            result, latency = await _invoke(name, {"project_id": project_id, "pipeline_id": pipeline_id})
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
    


