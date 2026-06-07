"""Dashboard read models — aggregates surfaced to the web client."""

from __future__ import annotations
from pydantic import BaseModel, Field
from app.schemas.diagnosis import RootCause  # reuse the canonical 5-category enum




class DashboardSummary(BaseModel):
    tests_fixed: int = Field(ge=0)
    fixed_this_week: int = Field(ge=0)
    success_rate: float = Field(ge=0.0, le=1.0)          # verifications passing the gate
    flakiness_rate: float = Field(ge=0.0, le=1.0)        # avg latest PFS / 100
    avg_fix_latency_ms: int = Field(ge=0)                # agent reasoning latency (not wall-clock)
    verifications_total: int = Field(ge=0)




class TrendPoint(BaseModel):
    day: str                     
    flakiness_rate: float = Field(ge=0.0, le=1.0)
    runs: int = Field(ge=0)       


class RootCauseSlice(BaseModel):
    category: RootCause
    count: int = Field(ge=0)


class ActivityItem(BaseModel):
    test_name: str
    file_path: str
    category: RootCause | None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    mr_iid: int | None
    mr_url: str | None
    created_at: str          
