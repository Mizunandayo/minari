"""Minari exposed as an mcp server"""



from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.session import init_pool
from app.mcp_server import tools

configure_logging(json_logs=get_settings().is_production)
log = get_logger("minari.mcp")
mcp = FastMCP(get_settings().mcp_server_name)






@mcp.tool()
async def detect(project_id: str, file_path: str, test_name: str) -> dict:
    """Compute the Probabilistic Flakiness Score for a test from its run history."""
    return await tools.detect(project_id, file_path, test_name)



@mcp.tool()
async def diagnose(project_id: str, file_path: str, test_name: str) -> dict:
    """diagnose the root cause of a flaky test"""
    return await tools.diagnose(project_id, file_path, test_name)




@mcp.tool()
async def fix(project_id: str, file_path: str, test_name: str) -> dict:
    """generate ranked candidate fixes for a flaky test"""
    return await tools.fix(project_id, file_path, test_name)



@mcp.tool()
async def verify(project_id: str, file_path: str, test_name: str) -> dict:
    """verify a fix by running it 5x in isolated CI"""
    return await tools.verify(project_id, file_path, test_name)



async def _bootstrap() -> None:
    await init_pool()
    log.info("mcp.server.ready", name=get_settings().mcp_server_name)