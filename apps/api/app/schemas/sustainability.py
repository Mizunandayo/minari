"""sustainability read model"""



from __future__ import annotations

from pydantic import BaseModel, Field


class CarbonReport(BaseModel):
    runs_avoided: int = Field(ge=0)
    ci_minutes_avoided: float = Field(ge=0)
    energy_kwh: float = Field(ge=0)
    co2_grams: float = Field(ge=0)
    engineer_hours_saved: float = Field(ge=0)
    grid_intensity_g_kwh: float = Field(ge=0)
    runner_power_kw: float = Field(ge=0)