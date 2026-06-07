import pytest

from app.agents.nodes.merger import merger_node
from app.agents.state import MinariState
from app.core.config import get_settings
from app.schemas.diagnosis import Diagnosis, ReasoningStep, RootCause
from app.schemas.fix import FixCandidate, FixCandidates, FixCategory
from app.schemas.verification import RunResult, VerificationReport


def _state(**kw) -> MinariState:
    diag = Diagnosis(category=RootCause.DATA, confidence=0.91,
                     reasoning_chain=[ReasoningStep(step=1, observation="shared table")],
                     triggering_lines=[12], affected_operations="db writes",
                     recommended_fix_category="isolate")
    fix = FixCandidate(rank=1, fix_category=FixCategory.ISOLATE, confidence=0.85,
                       explanation="scope per test", fixed_source="def t():\n assert 1\n",
                       syntax_valid=True, assertions_safe=True)
    ver = VerificationReport(branch_name="minari/fix-t-abcd1234", chosen_rank=1,
                             run_results=[RunResult(index=i, passed=True, duration_ms=100)
                                          for i in range(1, 6)],
                             pass_rate=1.0, gate_passed=True)
    base = dict(run_id="abcd1234-0000", project_id=get_settings().demo_project_id,
                file_path="tests/test_t.py", test_name="test_t", pfs_score=78,
                diagnosis=diag, fixes=FixCandidates(candidates=[fix]),
                verification=ver, status="verified")
    base.update(kw)
    return MinariState(**base)




@pytest.mark.asyncio
async def test_delivers_on_dry_run(monkeypatch):
    monkeypatch.setenv("MINARI_MERGER_DRY_RUN", "true")
    get_settings.cache_clear()
    out = await merger_node(_state())
    assert out.status == "delivered"
    assert out.merge is not None and out.merge.mr_iid == 0
    get_settings.cache_clear()




@pytest.mark.asyncio
async def test_refuses_unverified():
    out = await merger_node(_state(status="unverified",
                                   verification=VerificationReport(
                                       branch_name="x", gate_passed=False)))
    assert out.merge is None and out.status == "unverified"


@pytest.mark.asyncio
async def test_refuses_off_allowlist():
    out = await merger_node(_state(project_id="999/not-allowed"))
    assert out.merge is None