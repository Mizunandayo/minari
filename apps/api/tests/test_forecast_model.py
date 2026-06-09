from __future__ import annotations

from app.services.forecast.features import DailyPoint
from app.services.forecast.model import forecast


def _pts(rates: list[float]) -> list[DailyPoint]:
    return [DailyPoint(day=f"2026-06-{i+1:02d}", fail=round(r * 10), total=10)
            for i, r in enumerate(rates)]


def test_worsening_trend_is_high_risk() -> None:
    fc = forecast(_pts([0.1, 0.2, 0.4, 0.6, 0.7, 0.8]), horizon_days=7, min_runs=8)
    assert fc.trend == "worsening"
    assert fc.risk_tier in {"elevated", "high"}
    assert 0.0 <= fc.predicted_flakiness <= 1.0


def test_improving_trend_is_low_risk() -> None:
    fc = forecast(_pts([0.8, 0.6, 0.4, 0.2, 0.1, 0.05]), horizon_days=7, min_runs=8)
    assert fc.trend == "improving"
    assert fc.predicted_flakiness <= 0.5


def test_no_history_is_zero_confidence() -> None:
    fc = forecast([], horizon_days=7, min_runs=8)
    assert fc.confidence == 0.0
    assert fc.risk_tier == "low"


def test_prediction_always_in_unit_interval() -> None:
    fc = forecast(_pts([0.9] * 20), horizon_days=30, min_runs=8)
    assert 0.0 <= fc.predicted_flakiness <= 1.0
