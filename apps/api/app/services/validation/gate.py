"""the verification safety gate"""




from __future__ import annotations

from dataclasses import dataclass

from app.schemas.verification import RunResult
from app.services.validation.variance import mean_ms, reduction_pct, variance_ms


@dataclass(frozen=True)
class GateResult:
    passed: bool
    reason: str
    pass_rate: float
    variance_before: float
    variance_after: float
    variance_reduction_pct: float




def evaluate_gate(
    *,
    runs: list[RunResult],
    expected_runs: int,
    baseline_durations: list[float],
    min_variance_reduction: float,
    runtime_tolerance: float,
) -> GateResult:
    after_durations = [r.duration_ms for r in runs]
    v_before = variance_ms(baseline_durations)
    v_after = variance_ms(after_durations)
    reduction = reduction_pct(v_before, v_after)
    passes = sum(1 for r in runs if r.passed)
    pass_rate = passes / expected_runs if expected_runs else 0.0

    base = GateResult(False, "", pass_rate, v_before, v_after, reduction)

    if len(runs) < expected_runs or passes < expected_runs:
        return _with(base, reason=f"only {passes}/{expected_runs} runs passed")


    if v_before > 0 and reduction < min_variance_reduction:
        return _with(base, reason=(f"variance reduced {reduction * 100:.0f}% "
                                   f"(< {min_variance_reduction * 100:.0f}% required)"))


    base_avg = mean_ms(baseline_durations)
    after_avg = mean_ms(after_durations)
    if base_avg > 0 and after_avg > base_avg * runtime_tolerance:
        return _with(base, reason=(f"avg runtime {after_avg:.0f}ms exceeds "
                                   f"{runtime_tolerance:.1f}× baseline {base_avg:.0f}ms"))

    return _with(base, passed=True,
                 reason=f"5/5 passed · variance −{reduction * 100:.0f}%")


def _with(g: GateResult, *, passed: bool = False, reason: str = "") -> GateResult:
    return GateResult(passed, reason, g.pass_rate, g.variance_before,
                      g.variance_after, g.variance_reduction_pct)
