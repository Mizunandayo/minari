"""Duration variance"""

from __future__ import annotations

import statistics


def variance_ms(durations: list[float]) -> float:
    clean = [d for d in durations if d is not None and d >= 0]
    if len(clean) < 2:
        return 0.0
    return statistics.pvariance(clean)




def mean_ms(durations: list[float]) -> float:
    clean = [d for d in durations if d is not None and d >= 0]
    return statistics.fmean(clean) if clean else 0.0



def reduction_pct(before: float, after: float) -> float:
    """fraction of variance eliminated (0.0–1.0). 0.0 when there was no baseline."""
    if before <= 0:
        return 0.0
    return max(0.0, min(1.0, (before - after) / before))

