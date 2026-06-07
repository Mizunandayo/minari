"""Professional MR title / description / verification comment.
SECURITY: every interpolated value is sanitized to printable ASCII 
"""

from __future__ import annotations

import unicodedata

from app.schemas.diagnosis import Diagnosis
from app.schemas.fix import FixCandidate
from app.schemas.verification import VerificationReport
from app.services.delivery.confidence import Cascade

_CATEGORY_LABEL = {
    "async": "Async Timing",
    "race": "Race Condition",
    "resource": "Resource Contention",
    "network": "Network Flakiness",
    "data": "Data Isolation",
}





def to_ascii(text: str, *, limit: int = 4000) -> str:
    """Printable-ASCII only: NFKD-fold, drop non-ASCII, strip control chars
    (keeps \\n and \\t for markdown structure)."""
    folded = unicodedata.normalize("NFKD", text or "")
    out: list[str] = []
    for ch in folded:
        o = ord(ch)
        if ch in ("\n", "\t") or 32 <= o < 127:
            out.append(ch)
    return "".join(out).strip()[:limit]


def category_label(category: str) -> str:
    return _CATEGORY_LABEL.get(category, category.title())


def mr_labels(category: str) -> list[str]:
    return ["minari:auto-fix", "flaky-test",
            f"root-cause:{to_ascii(category, limit=24)}"]






def build_mr_title(test_name: str, category: str) -> str:
    return to_ascii(
        f"Fix flaky test: {test_name} - {category_label(category)}", limit=200)


def _variance_phrase(verification: VerificationReport) -> str:
    """Honest variance phrasing for the MR body. With no PFS history
    `variance_before == 0`, so the gate passes on the 'no prior variance' branch —
    reporting a reduction % there would read as if variance got worse. Say so plainly."""
    passed = sum(1 for r in verification.run_results if r.passed)
    total = len(verification.run_results)
    if verification.variance_before > 0:
        return (f"Variance reduced **{verification.variance_reduction_pct * 100:.0f}%** "
                f"({verification.variance_before:.0f} -> "
                f"{verification.variance_after:.0f} ms^2).")
    return (f"No pre-fix variance baseline available - gate passed on a clean "
            f"{passed}/{total} isolated pass (elimination, not reduction).")


def _variance_comment(verification: VerificationReport) -> str:
    """Short variance line for the MR note."""
    if verification.variance_before > 0:
        return f"Variance reduction: **{verification.variance_reduction_pct * 100:.0f}%**"
    return "Variance: no pre-fix baseline (gate passed on isolation)"


def build_mr_description(
    *, diagnosis: Diagnosis, fix: FixCandidate, verification: VerificationReport,
    cascade: Cascade, test_name: str, file_path: str, pfs_score: float,
    pipeline_url: str | None,
) -> str:
    cat = category_label(diagnosis.category.value)
    variance = _variance_phrase(verification)
    lines = diagnosis.triggering_lines or []
    line_str = ", ".join(str(n) for n in lines) if lines else "n/a"
    reasoning = "\n".join(
        f"  {i + 1}. {to_ascii(step.observation, limit=300)}"
        for i, step in enumerate(diagnosis.reasoning_chain[:6])
    ) or "  (no detailed reasoning recorded)"
    passed = sum(1 for r in verification.run_results if r.passed)
    total = len(verification.run_results)
    pipe = (f"\n> Verification pipeline: {to_ascii(pipeline_url, limit=300)}"
            if pipeline_url else "")

    body = f"""## Root Cause
**{cat}** (diagnosis confidence {diagnosis.confidence * 100:.0f}%)

Triggering line(s): `{line_str}` in `{to_ascii(file_path, limit=300)}`.

Reasoning chain:
```text
{reasoning}
```

## Evidence
- Probabilistic Flakiness Score (PFS): **{pfs_score:.0f}/100**
- Fix strategy: **{to_ascii(fix.fix_category.value, limit=24)}** (fix confidence {fix.confidence * 100:.0f}%)
- {to_ascii(fix.explanation, limit=600)}

## Fix
Minari rewrote `{to_ascii(test_name, limit=200)}` without modifying a single
assertion (AST-enforced: original assertions are a subset of the rewritten test).

## Verification
- **{passed}/{total}** isolated CI runs passed (fresh container per run, no cache, no parallelism).
- {variance}
- Safety gate: **{'PASSED' if verification.gate_passed else 'FAILED'}**.{pipe}

## Confidence Cascade
`detection {cascade.detection:.2f} x diagnosis {cascade.diagnosis:.2f} x fix {cascade.fix:.2f} x verification {cascade.verification:.2f}` = **{cascade.overall:.2f}**

**{to_ascii(cascade.tier, limit=80)}.**

---
*Opened by Minari. No human touched the code. Review and merge when satisfied.*
"""
    return to_ascii(body, limit=12000)






def build_verification_comment(
    verification: VerificationReport, cascade: Cascade,
) -> str:
    rows = "\n".join(
        f"| {r.index} | {'PASS' if r.passed else 'FAIL'} | {r.duration_ms:.0f} ms |"
        for r in verification.run_results
    ) or "| - | - | - |"
    body = f"""### Verification Report

| Run | Result | Duration |
|----:|:------:|---------:|
{rows}

- Pass rate: **{verification.pass_rate * 100:.0f}%**
- {_variance_comment(verification)}
- Healing attempts: **{verification.healing_attempts}**
- Overall confidence: **{cascade.overall * 100:.0f}%** ({to_ascii(cascade.tier, limit=80)})
"""
    return to_ascii(body, limit=6000)
