"""Consistent response envelope used by every endpoint"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")




class Envelope(BaseModel, Generic[T]):
    ok: bool = True
    data: T


class HealthChecks(BaseModel):
    db: str
    redis: str
    mcp: str


class HealthResponse(BaseModel):
    status: str
    checks: HealthChecks
