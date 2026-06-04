import pytest
from pydantic import ValidationError

from app.schemas.diagnosis import Diagnosis, RootCause


def _valid() -> dict:
    return {
        "category": "data",
        "confidence": 0.91,
        "reasoning_chain": [{"step": 1, "observation": "Two tests share a table."}],
        "triggering_lines": [42, 47],
        "affected_operations": "concurrent writes to checkout_items",
        "recommended_fix_category": "isolate",
    }


def test_valid_parses():
    d = Diagnosis.model_validate(_valid())
    assert d.category is RootCause.DATA
    assert d.is_confident is True


def test_extra_field_ignored():
    # Extra keys are dropped, not rejected (see Diagnosis note re: google-genai
    # response_schema). Required fields still validate.
    d = Diagnosis.model_validate({**_valid(), "sneaky": "x"})
    assert d.category is RootCause.DATA
    assert not hasattr(d, "sneaky")


def test_confidence_out_of_range_rejected():
    with pytest.raises(ValidationError):
        Diagnosis.model_validate({**_valid(), "confidence": 1.2})


def test_confidence_boundary():
    assert Diagnosis.model_validate({**_valid(), "confidence": 0.6}).is_confident is True
    assert Diagnosis.model_validate({**_valid(), "confidence": 0.59}).is_confident is False


def test_negative_line_rejected():
    with pytest.raises(ValidationError):
        Diagnosis.model_validate({**_valid(), "triggering_lines": [0]})
