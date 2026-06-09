"""flakiness forecaster projects the next-n-day flakiness probability"""




from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from app.services.forecast.features import DailyPoint, Features, extract_features

RiskTier = Literal["low", "elevated", "high"]
Trend = Literal["improving", "stable", "worsening"]



_RECENCY_WEIGHT = 0.45      
_STABLE_SLOPE = 0.003    






@dataclass(frozen=True)
class Forecast:
    predicted_flakiness: float   
    risk_tier: RiskTier
    trend: Trend
    confidence: float         
    drivers: list[str] 





def _logistic(x: float) -> float:
    x = max(-30.0, min(30.0, x))
    return 1.0 / (1.0 + math.exp(-x))




def _confidence(f: Features, min_runs: int) -> float:
    if f.n_runs <= 0:
        return 0.0
    base = f.n_runs / (f.n_runs + min_runs)
    return round(max(0.0, min(1.0, base * (1.0 - 0.5 * f.volatility))), 3)



def _drivers(f: Features) -> list[str]:
    out: list[str] = []
    if f.slope_per_day > _STABLE_SLOPE:
        out.append("worsening trend over the window")
    elif f.slope_per_day < -_STABLE_SLOPE:
        out.append("improving trend over the window")
    if f.recent_rate >= 0.30:
        out.append(f"high recent fail-rate ({f.recent_rate * 100:.0f}%)")
    if f.volatility >= 0.20:
        out.append("unstable run-to-run behavior")
    if f.n_runs < 8:
        out.append("limited run history — forecast is tentative")
    return out or ["stable, low-risk history"]




def forecast(points: list[DailyPoint], *, horizon_days: int, min_runs: int) -> Forecast:
    f: Features = extract_features(points)
    if f.n_runs == 0:
        return Forecast(0.0, "low", "stable", 0.0, ["no run history in the last 30 days"])


    projected_rate = f.recent_rate + f.slope_per_day * horizon_days
    blended = (1 - _RECENCY_WEIGHT) * projected_rate + _RECENCY_WEIGHT * f.recent_rate

    centered = (blended - 0.5) * 6.0   # spread around the 50% inflection
    predicted = round(_logistic(centered), 3)

    if abs(f.slope_per_day) < _STABLE_SLOPE:
        trend: Trend = "stable"
    else:
        trend = "worsening" if f.slope_per_day > 0 else "improving"

    if predicted >= 0.55:
        tier: RiskTier = "high"
    elif predicted >= 0.25:
        tier = "elevated"
    else:
        tier = "low"

    return Forecast(predicted, tier, trend, _confidence(f, min_runs), _drivers(f))