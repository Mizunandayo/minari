from app.services.delivery.confidence import cascade_confidence


def test_cascade_multiplies():
    c = cascade_confidence(pfs_score=78, diagnosis_confidence=0.91,
                           fix_confidence=0.85, pass_rate=1.0)
    assert abs(c.overall - (0.78 * 0.91 * 0.85 * 1.0)) < 1e-9


def test_cascade_clamps_out_of_range_inputs():
    c = cascade_confidence(pfs_score=150, diagnosis_confidence=2.0,
                           fix_confidence=-1.0, pass_rate=5.0)
    assert 0.0 <= c.overall <= 1.0


def test_tiers():
    assert cascade_confidence(pfs_score=100, diagnosis_confidence=1,
                              fix_confidence=1, pass_rate=1).tier.startswith("High")
    assert cascade_confidence(pfs_score=50, diagnosis_confidence=1,
                              fix_confidence=1, pass_rate=1).tier.startswith("Moderate")
    assert cascade_confidence(pfs_score=10, diagnosis_confidence=1,
                              fix_confidence=1, pass_rate=1).tier.startswith("Low")
