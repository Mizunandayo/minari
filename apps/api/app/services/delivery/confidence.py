"""Confidence cascade"""



from __future__ import annotations

from dataclasses import dataclass


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))




@dataclass(frozen=True)
class Cascade:
    detection: float
    diagnosis: float
    fix: float
    verification: float
    overall: float

    @property
    def tier(self) -> str:
        if self.overall >= 0.70:
            return "High - safe to merge"
        if self.overall >= 0.40:
            return "Moderate - review recommended"
        return "Low - manual review required"
    



def cascade_confidence(
    *, pfs_score: float, diagnosis_confidence: float,
    fix_confidence: float, pass_rate: float,
) -> Cascade:
    detection = _clamp(pfs_score / 100.0)
    diagnosis = _clamp(diagnosis_confidence)
    fix = _clamp(fix_confidence)
    verification = _clamp(pass_rate)
    overall = _clamp(detection * diagnosis * fix * verification)
    return Cascade(detection, diagnosis, fix, verification, overall)