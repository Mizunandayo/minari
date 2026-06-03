"""Probabilistic Flakiness Score (PFS) engine.

Pure Python with a single pure-Python dependency (defusedxml, for hardened XML
parsing) — runs identically on the CI runner edge module and in the cloud.
Score is 0–100:
    > 85  -> high-confidence FLAKY (escalate to diagnosis)
    < 20  -> high-confidence REAL BUG (do not auto-fix)
    20–85 -> UNCERTAIN (escalate to Gemini with full context)

Four weighted signals:
    pass_rate_flakiness  (0.40) — peaks at a 50% pass rate
    time_variance        (0.25) — normalized coefficient of variation of runtimes
    failure_entropy      (0.20) — Shannon entropy of failure positions across runs
    recency_bias         (0.15) — recent failures weighted above historical ones
"""




from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

# defusedxml hardens XML parsing against XXE / billion-laughs entity-expansion
# attacks. JUnit reports are attacker-influenceable (crafted report or test
# name), so we never use the stdlib parser on them. defusedxml is pure-Python,
# so the edge module stays dependency-light (no compiled extensions).
from defusedxml.ElementTree import fromstring as parse_xml_secure

WEIGHTS = {
    "pass_rate": 0.40,
    "variance": 0.25,
    "entropy": 0.20,
    "recency": 0.15,
}
MAX_HISTORY = 20





class Verdict(str, Enum):
    FLAKY = "flaky"
    NOT_FLAKY = "not_flaky"
    UNCERTAIN = "uncertain"






@dataclass(frozen=True)
class TestRun:
    __test__ = False  # not a pytest test class — this is a domain model
    passed: bool
    duration_ms: float





@dataclass(frozen=True)
class PFSResult:
    score: float
    verdict: Verdict
    pass_rate: float
    components: dict[str, float]





def _pass_rate_flakiness(runs: list[TestRun]) -> tuple[float, float]:
    if not runs:
        return 0.5, 0.5
    pass_rate = sum(1 for r in runs if r.passed) / len(runs)
    flakiness = 1.0 - abs(pass_rate - 0.5) * 2.0
    return max(0.0, flakiness), pass_rate






def _time_variance(runs: list[TestRun]) -> float:
    durations = [r.duration_ms for r in runs if r.duration_ms > 0]
    if len(durations) < 2:
        return 0.0
    mean = sum(durations) / len(durations)
    if mean == 0:
        return 0.0
    variance = sum((d - mean) ** 2 for d in durations) / len(durations)
    cv = math.sqrt(variance) / mean
    return min(1.0, cv)







def _failure_entropy(runs: list[TestRun]) -> float:
    n = len(runs)
    if n < 2:
        return 0.0
    failures = sum(1 for r in runs if not r.passed)
    if failures == 0 or failures == n:
        return 0.0 
    p_fail = failures / n
    p_pass = 1.0 - p_fail
    entropy = -(p_fail * math.log2(p_fail) + p_pass * math.log2(p_pass))
    return entropy




def _recency_bias(runs: list[TestRun]) -> float:
    n = len(runs)
    if n == 0:
        return 0.5
    weighted_fail, weight_total = 0.0, 0.0
    for i, run in enumerate(runs):
        weight = i + 1
        weight_total += weight
        if not run.passed:
            weighted_fail += weight
    return weighted_fail / weight_total if weight_total else 0.0






def calculate_pfs(runs: list[TestRun]) -> PFSResult:
    history = runs[-MAX_HISTORY:]
    if not history:
        return PFSResult(50.0, Verdict.UNCERTAIN, 0.5, {})

    flakiness, pass_rate = _pass_rate_flakiness(history)
    components = {
        "pass_rate": flakiness,
        "variance": _time_variance(history),
        "entropy": _failure_entropy(history),
        "recency": _recency_bias(history),
    }
    score = 100.0 * sum(components[k] * WEIGHTS[k] for k in WEIGHTS)
    score = round(max(0.0, min(100.0, score)), 1)



    if score > 85:
        verdict = Verdict.FLAKY
    elif score < 20:
        verdict = Verdict.NOT_FLAKY
    else:
        verdict = Verdict.UNCERTAIN



    return PFSResult(score, verdict, round(pass_rate, 3), components)






def parse_junit_xml(xml_bytes: bytes) -> dict[str, bool]:
    """Parse a single JUnit XML report -> {test_name: passed}."""
    results: dict[str, bool] = {}
    root = parse_xml_secure(xml_bytes)
    for case in root.iter("testcase"):
        name = case.get("name", "")
        failed = any(child.tag in {"failure", "error"} for child in case)
        if name:
            results[name] = not failed
    return results


    
