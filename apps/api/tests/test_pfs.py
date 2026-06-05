from app.services.pfs.engine import TestRun, Verdict, calculate_pfs


def _runs(spec: list[tuple[bool, int]]) -> list[TestRun]:
    return [TestRun(passed=p, duration_ms=d) for p, d in spec]






def test_known_flaky_returns_78_band():
    history = _runs([
        (True,198),(False,432),(True,205),(True,192),(False,445),
        (True,200),(False,418),(True,210),(True,195),(False,438),
        (False,425),(True,208),(False,440),(True,196),(False,420),
        (True,202),(False,448),(False,415),(True,212),(False,435),
    ])
    result = calculate_pfs(history)
    assert 73 <= result.score <= 83, result.score
    assert result.verdict == Verdict.UNCERTAIN





def test_all_pass_is_not_flaky():
    result = calculate_pfs(_runs([(True, 100)] * 20))
    assert result.verdict == Verdict.NOT_FLAKY
    assert result.score < 20





def test_all_fail_is_not_flaky_real_bug():
    result = calculate_pfs(_runs([(False, 100)] * 20))
    assert result.verdict == Verdict.NOT_FLAKY





def test_empty_history_is_uncertain():
    assert calculate_pfs([]).verdict == Verdict.UNCERTAIN




