from __future__ import annotations

from app.services.sustainability.carbon import CarbonInputs, estimate_savings


def test_zero_verifications_zero_savings() -> None:
    r = estimate_savings(CarbonInputs(0, 0, 4.0, 0.3, 480.0, 6.0))
    assert r.co2_grams == 0.0 and r.runs_avoided == 0


def test_savings_scale_with_verifications() -> None:
    r = estimate_savings(CarbonInputs(10, 5, 4.0, 0.3, 480.0, 6.0))
    assert r.runs_avoided == 50
    assert r.co2_grams > 0
    assert r.engineer_hours_saved == round((50 * 6.0) / 60.0, 1)
    assert r.grid_intensity_g_kwh == 480.0