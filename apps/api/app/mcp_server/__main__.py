"""Entrypoint: `python -m app.mcp_server` → stdio MCP server."""



from __future__ import annotations

import anyio

from app.mcp_server.server import _bootstrap, mcp

if __name__ == "__main__":
    anyio.run(_bootstrap)     
    mcp.run(transport="stdio")  