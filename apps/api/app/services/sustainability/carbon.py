"""carbon savings estimator closed form, pure, fully cited"""




from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CarbonInputs:
    verifications_passed: int
    runs_per_verification: float
    ci_minutes_per_run: float
    runner_power_kw: float
    grid_intensity_g_kwh: float
    engineer_minutes_per_run: float





@dataclass(frozen=True)
class CarbonReport:
    runs_avoided: int
    ci_minutes_avoided: float
    energy_kwh: float
    co2_grams: float
    engineer_hours_saved: float
    grid_intensity_g_kwh: float
    runner_power_kw: float





def estimate_savings(inp: CarbonInputs) -> CarbonReport:
    runs_avoided = round(inp.verifications_passed * inp.runs_per_verification)
    ci_minutes = runs_avoided * inp.ci_minutes_per_run
    energy_kwh = (ci_minutes / 60.0) * inp.runner_power_kw
    co2_grams = energy_kwh * inp.grid_intensity_g_kwh
    engineer_hours = (runs_avoided * inp.engineer_minutes_per_run) / 60.0
    return CarbonReport(
        runs_avoided=runs_avoided,
        ci_minutes_avoided=round(ci_minutes, 1),
        energy_kwh=round(energy_kwh, 4),
        co2_grams=round(co2_grams, 1),
        engineer_hours_saved=round(engineer_hours, 1),
        grid_intensity_g_kwh=inp.grid_intensity_g_kwh,
        runner_power_kw=inp.runner_power_kw,
    )
