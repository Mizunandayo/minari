from app.schemas.verification import RunResult
from app.services.validation.gate import evaluate_gate


def _runs(passes, dur=200.0):
    return [RunResult(index=i + 1, passed=p, duration_ms=dur) for i, p in enumerate(passes)]





def test_all_pass_low_variance_passes():
    g = evaluate_gate(runs=_runs([True] * 5), expected_runs=5,
                      baseline_durations=[100, 900, 100, 900],  
                      min_variance_reduction=0.8, runtime_tolerance=1.5)
    assert g.passed and g.pass_rate == 1.0


def test_one_failure_fails_gate():
    g = evaluate_gate(runs=_runs([True, True, True, True, False]), expected_runs=5,
                      baseline_durations=[200, 200], min_variance_reduction=0.8,
                      runtime_tolerance=1.5)
    assert not g.passed and "4/5" in g.reason




def test_insufficient_variance_reduction_fails():
    # baseline variance high, after variance still high ⇒ < 80% reduction
    g = evaluate_gate(runs=_runs([True] * 5, dur=0.0) 
                      , expected_runs=5, baseline_durations=[100, 900],
                      min_variance_reduction=0.8, runtime_tolerance=1.5)
    # craft non-collapsing after-variance
    g = evaluate_gate(
        runs=[RunResult(index=i + 1, passed=True, duration_ms=d)
              for i, d in enumerate([120, 880, 120, 880, 500])],
        expected_runs=5, baseline_durations=[100, 900],
        min_variance_reduction=0.8, runtime_tolerance=1.5)
    assert not g.passed and "variance" in g.reason




def test_no_baseline_variance_passes_on_all_pass():
    g = evaluate_gate(runs=_runs([True] * 5), expected_runs=5,
                      baseline_durations=[], min_variance_reduction=0.8,
                      runtime_tolerance=1.5)
    assert g.passed





def test_runtime_blowup_fails():
    g = evaluate_gate(
        runs=[RunResult(index=i + 1, passed=True, duration_ms=1000.0) for i in range(5)],
        expected_runs=5, baseline_durations=[100, 100],
        min_variance_reduction=0.8, runtime_tolerance=1.5)
    assert not g.passed and "runtime" in g.reason