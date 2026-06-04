"""Dashboard read endpoints (API-key protected)."""

from __future__ import annotations
from fastapi import APIRouter, Depends, Request
from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.core.security import require_api_key
from app.repositories.tests_repo import list_tests
from app.schemas.api import TestListItem
from app.schemas.common import Envelope


router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/tests", response_model=Envelope[list[TestListItem]])
@limiter.limit("60/minute")
async def list_project_tests(request: Request) -> Envelope[list[TestListItem]]:
    rows = await list_tests(get_settings().demo_project_id)
    return Envelope(data=[TestListItem(**r) for r in rows])
