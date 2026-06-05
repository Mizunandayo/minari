"""proof routes protected by demo api key"""



from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.core.config import get_settings
from app.core.rate_limit import DIAGNOSIS_LIMIT, limiter
from app.core.security import require_api_key
from app.schemas.common import Envelope
from app.services.gitlab_mcp import get_file_contents, list_tool_names

router = APIRouter(dependencies=[Depends(require_api_key)])





@router.get("/mcp/tools", response_model=Envelope[list[str]])
@limiter.limit("30/minute")
async def mcp_tools(request: Request) -> Envelope[list[str]]:
    return Envelope(data=await list_tool_names())





@router.get("/mcp/demo-file", response_model=Envelope[dict])
@limiter.limit(DIAGNOSIS_LIMIT)
async def mcp_demo_file(request: Request) -> Envelope[dict]:
    s = get_settings()
    content = await get_file_contents(s.demo_project_id, s.demo_test_file)
    body = str(content)
    return Envelope(
        data={
            "project_id": s.demo_project_id,
            "file_path": s.demo_test_file,
            "byte_length": len(body),
            "preview": body[:500],
        }
    )