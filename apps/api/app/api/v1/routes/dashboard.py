"""Dashboard read endpoints"""



from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.core.security import require_api_key
from app.repositories import analytics_repo, dashboard_repo
from app.schemas.common import Envelope
from app.schemas.dashboard import (
    ActivityItem,
    DashboardSummary,
    RootCauseSlice,
    TrendPoint,
)
from app.schemas.forecast import ForecastItem
from app.schemas.sustainability import CarbonReport
from app.services.forecast.features import DailyPoint
from app.services.forecast.model import forecast as run_forecast
from app.services.sustainability.carbon import CarbonInputs, estimate_savings

router = APIRouter(prefix="/dashboard", dependencies=[Depends(require_api_key)])



@router.get("/summary", response_model=Envelope[DashboardSummary])
@limiter.limit("60/minute")
async def summary(request: Request) -> Envelope[DashboardSummary]:
    data = await dashboard_repo.fetch_summary(get_settings().demo_project_id)
    return Envelope(data=DashboardSummary(**data))




@router.get("/trends", response_model=Envelope[list[TrendPoint]])
@limiter.limit("60/minute")
async def trends(request: Request) -> Envelope[list[TrendPoint]]:
    rows = await dashboard_repo.fetch_trends(get_settings().demo_project_id)
    return Envelope(data=[TrendPoint(**r) for r in rows])




@router.get("/root-causes", response_model=Envelope[list[RootCauseSlice]])
@limiter.limit("60/minute")
async def root_causes(request: Request) -> Envelope[list[RootCauseSlice]]:
    rows = await dashboard_repo.fetch_root_causes(get_settings().demo_project_id)
    return Envelope(data=[RootCauseSlice(**r) for r in rows])





@router.get("/activity", response_model=Envelope[list[ActivityItem]])
@limiter.limit("60/minute")
async def activity(request: Request) -> Envelope[list[ActivityItem]]:
    rows = await dashboard_repo.fetch_activity(get_settings().demo_project_id)
    return Envelope(data=[ActivityItem(**r) for r in rows])



 



@router.get("/forecast", response_model=Envelope[list[ForecastItem]])
@limiter.limit("60/minute")
async def forecast(request: Request) -> Envelope[list[ForecastItem]]:
    s = get_settings()
    history = await analytics_repo.fetch_test_daily_history(s.demo_project_id)
    items: list[ForecastItem] = []
    for key, rows in history.items():
        file_path, test_name = key.split("::", 1)
        points = [DailyPoint(day=r["day"], fail=r["fail"], total=r["total"]) for r in rows]
        fc = run_forecast(
            points,
            horizon_days=s.forecast_horizon_days,
            min_runs=s.forecast_min_runs,
        )
        items.append(
            ForecastItem(
                test_name=test_name,
                file_path=file_path,
                predicted_flakiness=fc.predicted_flakiness,
                risk_tier=fc.risk_tier,
                trend=fc.trend,
                confidence=fc.confidence,
                drivers=fc.drivers,
                horizon_days=s.forecast_horizon_days,
            )
        )
    # Highest-risk first — the demo opens on the scariest test.
    items.sort(key=lambda i: i.predicted_flakiness, reverse=True)
    return Envelope(data=items)






@router.get("/sustainability", response_model=Envelope[CarbonReport])
@limiter.limit("60/minute")
async def sustainability(request: Request) -> Envelope[CarbonReport]:
    s = get_settings()
    raw = await analytics_repo.fetch_savings_inputs(s.demo_project_id)
    report = estimate_savings(
        CarbonInputs(
            verifications_passed=raw["verifications_passed"],
            runs_per_verification=raw["runs_per_verification"],
            ci_minutes_per_run=s.carbon_ci_minutes_per_run,
            runner_power_kw=s.carbon_runner_power_kw,
            grid_intensity_g_kwh=s.carbon_grid_intensity_g_kwh,
            engineer_minutes_per_run=s.carbon_engineer_minutes_per_run,
        )
    )
    return Envelope(data=CarbonReport(**report.__dict__))