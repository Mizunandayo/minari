from __future__ import annotations
from fastapi import APIRouter
from app.api.v1.routes import health, mcp_demo





api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(health.router, tags=["health"])
api_v1.include_router(mcp_demo.router, tags=["mcp"])

