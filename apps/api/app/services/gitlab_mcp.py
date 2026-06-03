"""GitLab MCP Server client.

Uses the community ``@zereight/mcp-gitlab`` server (Node, launched over stdio),
which wraps the GitLab REST API and authenticates with a Personal Access Token.
The official hosted GitLab MCP (/api/v4/mcp) requires Premium/Ultimate + GitLab
Duo + OAuth 2.0 DCR, so it is not usable on a free account — this server is the
free, PAT-based path and matches the blueprint's "GitLab MCP Server 0.4+".
"""

from __future__ import annotations

import os
import sys
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

    # Windows (local dev): launch the server via npx through cmd.exe.
    # POSIX/container: call the globally-installed binary directly (the Dockerfile
    # symlinks it to /usr/local/bin/minari-mcp). npx is avoided in the container
    # because it ignores global installs and re-downloads from the registry.
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
                # Merge os.environ so npx inherits PATH/SystemRoot, then add the
                # GitLab credentials the server reads.
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