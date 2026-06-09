"""feature extraction for flakiness forecasting"""




from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DailyPoint:
    day: str
    fail: int
    total: int

    @property
    def rate(self) -> float:
        return (self.fail / self.total) if self.total else 0.0
    





@dataclass(frozen=True)
class Features:
    n_days: int         
    n_runs: int           
    mean_rate: float      
    recent_rate: float      
    slope_per_day: float    
    volatility: float       





def _ols_slope(xs: list[float], ys: list[float]) -> float:
    """ordinary-least-squares slope"""
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    return num / denom







def extract_features(points: list[DailyPoint]) -> Features:
    active = [p for p in points if p.total > 0]
    if not active:
        return Features(0, 0, 0.0, 0.0, 0.0, 0.0)

    rates = [p.rate for p in active]
    xs = [float(i) for i in range(len(active))]
    mean_rate = sum(rates) / len(rates)
    recent = rates[-7:]
    recent_rate = sum(recent) / len(recent)
    slope = _ols_slope(xs, rates)
    variance = sum((r - mean_rate) ** 2 for r in rates) / len(rates)
    return Features(
        n_days=len(active),
        n_runs=sum(p.total for p in active),
        mean_rate=mean_rate,
        recent_rate=recent_rate,
        slope_per_day=slope,
        volatility=math.sqrt(variance),
    )