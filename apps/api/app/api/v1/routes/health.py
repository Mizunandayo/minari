"""Health endpoint"""


from __future__ import annotations
from fastapi import APIRouter
from app.db.session import ping_db
from app.schemas.common import HealthChecks, HealthResponse
from app.services.gitlab_mcp import ping_mcp




router = APIRouter()



async def _ping_redis() -> bool:
    import redis.asyncio as aioredis
    from app.core.config import get_settings

    client = aioredis.from_url(get_settings().redis_url.get_secret_value())
    try:
        return await client.ping()
    except Exception:
        return False
    finally:
        await client.close()







@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    db_ok = await ping_db()
    redis_ok = await _ping_redis()
    mcp_ok = await ping_mcp()
    overall = "ok" if (db_ok and redis_ok and mcp_ok) else "degraded"
    return HealthResponse(
        status=overall,
        checks=HealthChecks(
            db="ok" if db_ok else "fail",
            redis="ok" if redis_ok else "fail",
            mcp="ok" if mcp_ok else "fail",
        ),
    )
