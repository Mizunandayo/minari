from app.schemas.diagnosis import Diagnosis, ReasoningStep, RootCause
from app.schemas.fix import FixCandidate, FixCategory
from app.schemas.verification import RunResult, VerificationReport
from app.services.delivery.confidence import cascade_confidence
from app.services.delivery.mr_description import (
    build_mr_description,
    build_mr_title,
    to_ascii,
)


def test_to_ascii_drops_non_ascii():
    assert to_ascii("em\u2014dash \u201cq\u201d") == "emdash q"


def test_to_ascii_blocks_control_chars():
    assert "\x00" not in to_ascii("a\x00b")




def _diag() -> Diagnosis:
    return Diagnosis(
        category=RootCause.DATA, confidence=0.91,
        reasoning_chain=[ReasoningStep(step=1, observation="shared table no isolation")],
        triggering_lines=[12], affected_operations="db writes",
        recommended_fix_category="isolate",
    )



def test_description_is_ascii_and_has_sections():
    diag = _diag()
    fix = FixCandidate(rank=1, fix_category=FixCategory.ISOLATE, confidence=0.85,
                       explanation="scope the table per test invocation",
                       fixed_source="def test_x():\n    assert True\n")
    ver = VerificationReport(branch_name="minari/fix-x-abcd1234", chosen_rank=1,
                             run_results=[RunResult(index=i, passed=True, duration_ms=200)
                                          for i in range(1, 6)],
                             pass_rate=1.0, variance_before=34.0, variance_after=0.0,
                             variance_reduction_pct=1.0, gate_passed=True)
    casc = cascade_confidence(pfs_score=78, diagnosis_confidence=0.91,
                              fix_confidence=0.85, pass_rate=1.0)
    body = build_mr_description(diagnosis=diag, fix=fix, verification=ver, cascade=casc,
                                test_name="test_x", file_path="tests/test_x.py",
                                pfs_score=78, pipeline_url=None)
    assert body.isascii()
    for section in ("## Root Cause", "## Evidence", "## Fix",
                    "## Verification", "## Confidence Cascade"):
        assert section in body




def _ver(*, variance_before: float, variance_after: float, pct: float) -> VerificationReport:
    return VerificationReport(
        branch_name="minari/fix-x-abcd1234", chosen_rank=1,
        run_results=[RunResult(index=i, passed=True, duration_ms=200) for i in range(1, 6)],
        pass_rate=1.0, variance_before=variance_before, variance_after=variance_after,
        variance_reduction_pct=pct, gate_passed=True)


def _build(ver: VerificationReport) -> str:
    fix = FixCandidate(rank=1, fix_category=FixCategory.ISOLATE, confidence=0.85,
                       explanation="scope the table per test invocation",
                       fixed_source="def test_x():\n    assert True\n")
    casc = cascade_confidence(pfs_score=50, diagnosis_confidence=1.0,
                              fix_confidence=1.0, pass_rate=1.0)
    return build_mr_description(diagnosis=_diag(), fix=fix, verification=ver, cascade=casc,
                               test_name="test_x", file_path="tests/test_x.py",
                               pfs_score=50, pipeline_url=None)


def test_no_baseline_variance_copy_is_honest():
    # The real live case: no PFS history -> variance_before == 0. The body must NOT
    # claim a misleading "reduced 0% (0 -> big)"; it should state there's no baseline.
    body = _build(_ver(variance_before=0.0, variance_after=952775.0, pct=0.0))
    assert "No pre-fix variance baseline available" in body
    assert "Variance reduced" not in body
    assert "0 ->" not in body


def test_with_baseline_reports_reduction():
    body = _build(_ver(variance_before=34.0, variance_after=2.0, pct=0.94))
    assert "Variance reduced **94%**" in body


def test_title_blocks_markdown_injection():
    # A crafted test name cannot smuggle non-ascii or break the title line.
    t = build_mr_title("test_x\u202e evil", "data")
    assert t.isascii() and "\n" not in t