"""forecast read model surfaced to the dashboard"""


from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ForecastItem(BaseModel):
    test_name: str
    file_path: str
    predicted_flakiness: float = Field(ge=0.0, le=1.0)
    risk_tier: Literal["low", "elevated", "high"]
    trend: Literal["improving", "stable", "worsening"]
    confidence: float = Field(ge=0.0, le=1.0)
    drivers: list[str]
    horizon_days: int = Field(ge=1)